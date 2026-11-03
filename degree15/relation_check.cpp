#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <algorithm>
using V=std::array<uint64_t,8>;
int main(int argc,char**argv){if(argc!=2)return 2;std::ifstream f(argv[1]);int ind,d,n;f>>ind>>d>>n;if(!f||n>32||d>32)return 2;V r[32],v{};for(int j=0;j<n;j++)for(auto &x:r[j])f>>x;if(!f)return 2;uint64_t stop=uint64_t(1)<<n;for(uint64_t k=1;k<stop;k++){int t=__builtin_ctzll(k);for(int j=0;j<8;j++)v[j]^=r[t][j];uint64_t a=v[0]&((uint64_t(1)<<d)-1);int mx=a?64-__builtin_clzll(a):0;int sum=0;for(int j=0;j<ind-1;j++){int pos=d+((d-2)/2)*j,off=pos%64;a=v[pos/64]>>off;if(off+((d-2)/2)>64)a|=v[pos/64+1]<<(64-off);a&=(uint64_t(1)<<((d-2)/2))-1;int m=a?64-__builtin_clzll(a):0;mx=std::max(mx,m);sum+=m;if(sum+mx>d)break;}if(sum+mx<=d){std::cout<<"FAIL relation="<<k<<" cost="<<sum+mx<<"\n";return 1;}}std::cout<<"PASS relations="<<n<<" tested="<<stop-1<<"\n";}
