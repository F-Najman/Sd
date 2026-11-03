#include <array>
#include <vector>
#include <fstream>
#include <iostream>
#include <cstdint>
#include <algorithm>
#include <chrono>
using V=std::array<uint64_t,16>;
int top(const V&v){for(int k=15;k>=0;--k)if(v[k])return 64*k+63-__builtin_clzll(v[k]);return -1;}
struct Basis{std::array<V,1024>v{};bool used[1024]{};std::vector<int>hist;bool add(V x){int k;while((k=top(x))>=0){if(!used[k]){v[k]=x;used[k]=true;hist.push_back(k);return true;}for(int j=0;j<16;++j)x[j]^=v[k][j];}return false;}void undo(int n){while((int)hist.size()>n){used[hist.back()]=false;hist.pop_back();}}};
std::vector<V>rows;std::vector<int>sizes;Basis bs;int m,d,mod,first;uint64_t count=0;bool fail=false;
int rels(){int total=0;for(int r=0;r<mod;++r){int z=d;for(int j=r;j<m;j+=mod)z=std::min(z,sizes[j]);total+=z;}return total;}
void dfs(int pos,int remain){if(fail)return;if(pos==m){if(remain==0)++count;return;}int mx=std::min(first,remain);if(remain>(m-pos)*mx)return;int old=bs.hist.size();sizes[pos]=0;dfs(pos+1,remain);for(int k=1;k<=mx&&!fail;++k){int before=rels();sizes[pos]=k;int after=rels();bool independent=bs.add(rows[pos*d+k-1]);if(independent!=(after==before)){fail=true;std::cout<<"UNEXPECTED_RELATION pos="<<pos<<" multiplicity="<<k<<" remaining="<<remain-k<<" expected_defect="<<after<<" sizes=";for(int z:sizes)std::cout<<z<<",";std::cout<<"\n";break;}dfs(pos+1,remain-k);}sizes[pos]=0;bs.undo(old);}
int main(int argc,char**argv){std::ifstream f(argv[1]);f>>m>>d>>mod;rows.resize(m*d);for(auto&v:rows)for(auto&x:v)f>>x;sizes.assign(m,0);auto t=std::chrono::steady_clock::now();for(first=1;first<=d&&!fail;++first){bs=Basis{};sizes.assign(m,0);bool ok=true;for(int k=1;k<=first;++k){sizes[0]=k;if(!bs.add(rows[k-1]))ok=false;}if(!ok){fail=true;break;}dfs(1,d-first);std::cerr<<"prefix="<<first<<" count="<<count<<"\n";}std::cout<<"S17_RELATIVE_PREFIX_CHECK checked="<<count<<" status="<<(fail?"FAIL":"PASS")<<" seconds="<<std::chrono::duration<double>(std::chrono::steady_clock::now()-t).count()<<"\n";return fail?1:0;}
