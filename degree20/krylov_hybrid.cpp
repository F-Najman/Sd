#include <algorithm>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <numeric>
#include <string>
#include <vector>
using namespace std;
int main(int argc,char**argv){
 assert(argc>=3&&argc<=5);auto start=chrono::steady_clock::now();ifstream in(argv[1]);assert(in);uint64_t q;size_t n,k,nnz;in>>q>>n>>k>>nnz;
 assert(q>3&&q<=numeric_limits<uint32_t>::max()&&n<numeric_limits<uint32_t>::max()&&n>k&&n*((__uint128_t)(q-1)*(q-1))<=numeric_limits<uint64_t>::max());
 size_t steps=argc>=4?stoull(argv[3]):2*k;unsigned threshold=argc>=5?stoul(argv[4]):500;assert(steps>=64&&steps<=2*k&&threshold>=1&&threshold<=1000);
 vector<uint32_t>v(n),u(n),w(n);for(auto&x:v){in>>x;assert(x<q);}for(auto&x:u){in>>x;assert(x<q);}
 vector<uint32_t>col(nnz),val(nnz),seen(n,0);vector<size_t>rowoff(n+1);size_t count=0;
 for(size_t i=0;i<n;i++){size_t z;in>>z;assert(z<=n);rowoff[i]=count;
  for(size_t j=0;j<z;j++){uint32_t c,a;in>>c>>a;assert(c<n&&a>0&&a<q&&count<nnz&&seen[c]!=i+1);seen[c]=i+1;col[count]=c;val[count]=a;count++;}
 }rowoff[n]=count;assert(count==nnz&&in);
 size_t checkn;in>>checkn;assert(checkn==64);vector<uint32_t>checks(checkn);for(auto&x:checks){in>>x;assert(x<q);}string extra;assert(in&&!(in>>extra));
 vector<int>denseindex(n,-1);vector<uint32_t>denserows;
 for(size_t i=0;i<n;i++)if((rowoff[i+1]-rowoff[i])*1000>=threshold*n){denseindex[i]=denserows.size();denserows.push_back(i);}
 size_t nd=denserows.size();assert(nd==0||n<=numeric_limits<size_t>::max()/nd);vector<uint32_t>dense(n*nd,0);vector<size_t>off(n+1,0);size_t sparsecount=0;
 for(size_t i=0;i<n;i++)for(size_t h=rowoff[i];h<rowoff[i+1];h++){
  if(denseindex[i]>=0)dense[col[h]*nd+denseindex[i]]=val[h];else{off[col[h]+1]++;sparsecount++;}
 }
 partial_sum(off.begin(),off.end(),off.begin());auto pos=off;assert(n<=numeric_limits<uint16_t>::max());vector<uint16_t>src(sparsecount);vector<uint32_t>coef(sparsecount);
 for(size_t i=0;i<n;i++)if(denseindex[i]<0)for(size_t h=rowoff[i];h<rowoff[i+1];h++){auto j=pos[col[h]]++;src[j]=i;coef[j]=val[h];}
 for(size_t j=0;j<n;j++)assert(nd+off[j+1]-off[j]<=n);
 vector<uint32_t>().swap(col);vector<uint32_t>().swap(val);vector<uint32_t>().swap(seen);vector<size_t>().swap(rowoff);vector<int>().swap(denseindex);vector<size_t>().swap(pos);
 vector<uint32_t>vd(nd);ofstream out(argv[2]);assert(out);out<<"q:="<<q<<";dimension:="<<k<<";sequence:=[";
 cout<<"S20_HYBRID_MATRIX original_nnz="<<nnz<<" dense_rows="<<nd<<" dense_words="<<dense.size()<<" sparse_nnz="<<sparsecount<<" threshold_per_mille="<<threshold<<endl;
 auto calc=chrono::steady_clock::now();
 for(size_t step=0;step<steps;step++){
  uint64_t dot=0;for(size_t j=0;j<n;j++)dot+=(uint64_t)v[j]*u[j];uint32_t s=dot%q;if(step<checkn)assert(s==checks[step]);if(step)out<<',';out<<s;
  for(size_t i=0;i<nd;i++)vd[i]=v[denserows[i]];
  for(size_t j=0;j<n;j++){
   uint64_t a=0;const uint32_t*base=(nd?dense.data()+j*nd:nullptr);
   for(size_t i=0;i<nd;i++)a+=(uint64_t)base[i]*vd[i];
   for(size_t h=off[j];h<off[j+1];h++)a+=(uint64_t)v[src[h]]*coef[h];
   w[j]=a%q;
  }v.swap(w);
 }out<<"];\n";out.close();
 cout<<(steps==2*k?"S20_CPP_KRYLOV_COMPLETE":"S20_CPP_KRYLOV_PREFIX_BENCHMARK")<<" q="<<q<<" ambient_dimension="<<n<<" dimension="<<k<<" nnz="<<nnz<<" native_prefix_checked="<<checkn<<" steps="<<steps<<" implementation=hybrid_dense_rows_v1 compute_seconds="<<chrono::duration<double>(chrono::steady_clock::now()-calc).count()<<" total_seconds="<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<endl;
}
