#include <array>
#include <vector>
#include <fstream>
#include <iostream>
#include <cstdint>
using V=std::array<uint64_t,16>;
int top(const V&v){for(int k=15;k>=0;--k)if(v[k])return 64*k+63-__builtin_clzll(v[k]);return -1;}
struct Basis{std::array<V,1024>v{};bool used[1024]{};std::vector<int>hist;bool add(V x){int k;while((k=top(x))>=0){if(!used[k]){v[k]=x;used[k]=true;hist.push_back(k);return true;}for(int j=0;j<16;++j)x[j]^=v[k][j];}return false;}void undo(int n){while((int)hist.size()>n){used[hist.back()]=false;hist.pop_back();}}};
V cols[26][19];std::vector<std::array<int,13>>patterns;std::array<int,26>mult;uint64_t checked=0,relative=0,bad=0;Basis B;std::array<int,13>pat;
void dfs(int pos){if(pos==13){++checked;int r=19;int mn[2]={19,19};for(int j=0;j<26;j++)mn[j%2]=std::min(mn[j%2],mult[j]);r-=mn[0]+mn[1];if((int)B.hist.size()!=r){++bad;if(bad<4){std::cout<<"BAD ";for(auto a:mult)std::cout<<a<<",";std::cout<<" rank="<<B.hist.size()<<" expected="<<r<<"\n";}}if(r<19)++relative;return;}int old=B.hist.size();for(int a=0;a<=pat[pos];a++){mult[pos]=a;mult[pos+13]=pat[pos]-a;for(int j=0;j<a;j++)B.add(cols[pos][j]);for(int j=0;j<pat[pos]-a;j++)B.add(cols[pos+13][j]);dfs(pos+1);B.undo(old);}}
int main(int argc,char**argv){std::ifstream f(argv[1]);int n;f>>n;patterns.resize(n);for(auto &p:patterns)for(auto &x:p)f>>x;for(auto &c:cols)for(auto &v:c)for(auto &x:v)f>>x;for(auto &p:patterns){pat=p;B=Basis{};dfs(0);}std::cout<<"S19_CUSPS53_CHECK checked="<<checked<<" relative="<<relative<<" bad="<<bad<<" status="<<(bad?"FAIL":"PASS")<<"\n";return bad?1:0;}
