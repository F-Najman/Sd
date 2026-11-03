#include <algorithm>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <numeric>
#include <vector>
using namespace std;
int main(int argc,char**argv){
 assert(argc==3);ifstream in(argv[1]);assert(in);uint64_t q;size_t n,k,nnz;in>>q>>n>>k>>nnz;assert(q>3&&q<=numeric_limits<uint32_t>::max()&&n<numeric_limits<uint32_t>::max()&&n>k);
 size_t block=numeric_limits<uint64_t>::max()/((__uint128_t)(q-1)*(q-1));assert(block>0);
 vector<uint32_t>v(n),u(n),w(n);for(auto &x:v){in>>x;assert(x<q);}for(auto &x:u){in>>x;assert(x<q);}
 vector<uint32_t>ri(nnz),ci(nnz),val(nnz);vector<size_t>off(n+1);size_t count=0;
 vector<uint32_t>seen(n,0);
 for(size_t i=0;i<n;i++){size_t z;in>>z;assert(z<=n);for(size_t j=0;j<z;j++){uint32_t c,a;in>>c>>a;assert(c<n&&a>0&&a<q&&count<nnz&&seen[c]!=i+1);seen[c]=i+1;ri[count]=i;ci[count]=c;val[count]=a;off[c+1]++;count++;}}assert(count==nnz&&in);
 partial_sum(off.begin(),off.end(),off.begin());auto pos=off;vector<uint32_t>src(nnz),coef(nnz);
 for(size_t i=0;i<nnz;i++){auto j=pos[ci[i]]++;src[j]=ri[i];coef[j]=val[i];}ri.clear();ci.clear();val.clear();
 size_t maxcol=0;for(size_t j=0;j<n;j++)maxcol=max(maxcol,off[j+1]-off[j]);bool safe_columns=maxcol*((__uint128_t)(q-1)*(q-1))<=numeric_limits<uint64_t>::max();
 size_t checkn;in>>checkn;assert(checkn==64);vector<uint32_t>checks(checkn);for(auto &x:checks)in>>x;assert(in);string extra;assert(!(in>>extra));
 ofstream out(argv[2]);assert(out);out<<"q:="<<q<<";dimension:="<<k<<";sequence:=[";
 for(size_t step=0;step<2*k;step++){
  uint64_t dot=0;for(size_t lo=0;lo<n;lo+=block){uint64_t part=0;for(size_t j=lo;j<min(n,lo+block);j++)part+=(uint64_t)v[j]*u[j];dot=(dot+part%q)%q;}uint32_t s=dot;if(step<checkn)assert(s==checks[step]);if(step)out<<',';out<<s;
  for(size_t j=0;j<n;j++){uint64_t a=0;if(safe_columns){for(size_t h=off[j];h<off[j+1];h++)a+=(uint64_t)v[src[h]]*coef[h];w[j]=a%q;}else{for(size_t lo=off[j];lo<off[j+1];lo+=block){uint64_t part=0;for(size_t h=lo;h<min(off[j+1],lo+block);h++)part+=(uint64_t)v[src[h]]*coef[h];a=(a+part%q)%q;}w[j]=a;}}v.swap(w);
 }out<<"];\n";out.close();cout<<"S21_CPP_BLOCKED_KRYLOV_COMPLETE q="<<q<<" ambient_dimension="<<n<<" dimension="<<k<<" nnz="<<nnz<<" native_prefix_checked="<<checkn<<endl;
}
