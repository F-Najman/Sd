#include <array>
#include <vector>
#include <fstream>
#include <iostream>
#include <string>
#include <cstdint>
#include <chrono>
using V=std::array<uint64_t,8>;
int top(const V&v){for(int k=7;k>=0;--k)if(v[k])return 64*k+63-__builtin_clzll(v[k]);return -1;}
struct Basis{std::array<V,512> v{};bool used[512]{};std::vector<int> hist; bool add(V x){int k;while((k=top(x))>=0){if(!used[k]){v[k]=x;used[k]=true;hist.push_back(k);return true;}for(int j=0;j<8;++j)x[j]^=v[k][j];}return false;}void undo(int n){while((int)hist.size()>n){used[hist.back()]=false;hist.pop_back();}}};
std::vector<V> rows; int ind,d,cap,first;uint64_t count=0; std::vector<int> sizes;bool failure=false;Basis bs;
void dfs(int pos,int remain){if(failure)return;if(pos==ind){if(remain==0)++count;return;}int max=std::min(std::min(first,cap),remain);if(remain>(ind-pos)*max)return;int old=bs.hist.size();for(int m=0;m<=max;++m){if(m){int k=d+(pos-1)*cap+m-1;if(!bs.add(rows[k])){if(remain-m<=(ind-pos-1)*std::min(first,cap)){failure=true;sizes[pos]=m;std::cout<<"DEPENDENT_PREFIX ";for(int q=0;q<=pos;++q)std::cout<<sizes[q]<<",";std::cout<<" remaining="<<remain-m<<"\n";}break;}}sizes[pos]=m;dfs(pos+1,remain-m);}bs.undo(old);}
int main(int argc,char**argv){std::ifstream f(argv[1]);int p,tn,gen,nr,nc,rank;f>>p>>ind>>tn>>gen>>nr>>nc>>d>>rank;cap=(d-1)/2;rows.resize(nr);for(auto&v:rows)for(auto&x:v)f>>x;sizes.resize(ind);auto t=std::chrono::steady_clock::now();for(first=1;first<=d&&!failure;++first){bs=Basis{};bool ok=true;for(int i=0;i<first;++i)if(!bs.add(rows[i]))ok=false;if(!ok){failure=true;break;}sizes[0]=first;dfs(1,d-first);std::cerr<<"prefix="<<first<<" count="<<count<<"\n";}std::cout<<"DECIC_PREFIX_CHECK level="<<p<<" degree="<<d<<" rank="<<rank<<" checked="<<count<<" status="<<(failure?"FAIL":"PASS")<<" seconds="<<std::chrono::duration<double>(std::chrono::steady_clock::now()-t).count()<<"\n";return failure?1:0;}
