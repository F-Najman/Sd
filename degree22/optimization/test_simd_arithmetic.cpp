#include <immintrin.h>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <random>
#include <vector>
using namespace std;
int main(){mt19937_64 rng(22022022);size_t total=0;
 for(uint64_t q:vector<uint64_t>{5,7,101,65537,262139,1048573,6297589,16777213,536870909}){
  unsigned B=32;__uint128_t bound=(__uint128_t)4*(q-1)*(q-1);while(B<64&&((__uint128_t)1<<B)<=bound)++B;
  uint64_t mu=uint64_t(((__uint128_t)1<<B)/q);assert(B<64&&mu<=UINT32_MAX&&4*(q-1)<UINT32_MAX);
  __m512i vm=_mm512_set1_epi64(mu),vq=_mm512_set1_epi64(q);__m128i shift=_mm_cvtsi64_si128(B-32);
  alignas(64)uint64_t zz[8],rr[8];
  for(size_t t=0;t<100000;++t){
   for(size_t i=0;i<8;++i){uint64_t z=0;for(int j=0;j<4;++j)z+=(rng()%q)*(rng()%q);zz[i]=z;}
   if(t<10)for(size_t i=0;i<8;++i)zz[i]=t==0?0:t==1?uint64_t(bound):t==2?uint64_t(bound)-i:t==3?q*i:t==4?q*i+1:t==5?q*(i+1)-1:zz[i];
   __m512i z=_mm512_load_si512(zz),zl=_mm512_mul_epu32(z,vm),zh=_mm512_mul_epu32(_mm512_srli_epi64(z,32),vm);
   __m512i h=_mm512_srl_epi64(_mm512_add_epi64(zh,_mm512_srli_epi64(zl,32)),shift),r=_mm512_sub_epi64(z,_mm512_mul_epu32(h,vq));
   __mmask8 ge=_mm512_cmp_epu64_mask(r,vq,_MM_CMPINT_NLT);r=_mm512_mask_sub_epi64(r,ge,r,vq);_mm512_store_si512(rr,r);
   for(size_t i=0;i<8;++i)assert(rr[i]==zz[i]%q);total+=8;
  }
 }
 cout<<"S22_SIMD_EXACT_INTEGER_REDUCTION_PASS cases="<<total<<endl;
}
