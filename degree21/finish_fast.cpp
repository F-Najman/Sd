#include <NTL/lzz_pX.h>
#include <cassert>
#include <fstream>
#include <iostream>
#include <iterator>
#include <cctype>
#include <cstdint>
#include <vector>
using namespace NTL;using namespace std;
int main(int argc,char**argv){
 assert(argc==4);ifstream in(argv[1]);assert(in);string s((istreambuf_iterator<char>(in)),istreambuf_iterator<char>());
 auto scalar=[&](const string&name){size_t j=s.find(name+":=");assert(j!=string::npos);j+=name.size()+2;assert(isdigit(s[j]));uint64_t v=0;while(isdigit(s[j])){v=10*v+s[j++]-'0';}assert(s[j]==';');return v;};
 uint64_t q=scalar("q");long k=scalar("dimension");assert(q>3&&q<UINT32_MAX&&k>0);zz_p::init(q);size_t j=s.find("sequence:=[");assert(j!=string::npos);j+=11;vector<long>seq;
 while(true){while(isspace(s[j]))j++;assert(isdigit(s[j]));uint64_t a=0;while(isdigit(s[j]))a=10*a+s[j++]-'0';assert(a<q);seq.push_back(a);while(isspace(s[j]))j++;if(s[j]==']')break;assert(s[j++]==',');}assert(seq.size()==size_t(2*k));
 zz_pX S,U,V,C,A;for(long i=0;i<2*k;i++)SetCoeff(S,i,seq[i]);SetCoeff(U,2*k);V=S;
 if(deg(V)>=k){zz_pXMatrix M;XHalfGCD(M,U,V,k+1);C=M(1,1);A=V;}else{SetCoeff(C,0);A=S;}
 assert(!IsZero(coeff(C,0)));zz_p c=inv(coeff(C,0));C*=c;A*=c;assert(IsOne(coeff(C,0))&&deg(C)<=k&&deg(A)<k&&max(deg(C),deg(A)+1)==k);assert(IsOne(GCD(C,A)));zz_pX error=C*S-A;trunc(error,error,2*k);assert(IsZero(error));
 ofstream f(argv[2]);assert(f);f<<"q:="<<q<<";dimension:="<<k<<";linear_complexity:="<<k<<";sequence:=[";for(size_t i=0;i<seq.size();i++){if(i)f<<',';f<<seq[i];}f<<"];recurrence:=[";for(long i=0;i<=deg(C);i++){if(i)f<<',';f<<rep(coeff(C,i));}f<<"];\n";f.close();
 ofstream g(argv[3]);assert(g);g<<"{\"q\":"<<q<<",\"dimension\":"<<k<<",\"complexity\":"<<k<<",\"C\":[";for(long i=0;i<=deg(C);i++){if(i)g<<',';g<<rep(coeff(C,i));}g<<"],\"A\":[";for(long i=0;i<=deg(A);i++){if(i)g<<',';g<<rep(coeff(A,i));}g<<"],\"algorithm\":\"NTL XHalfGCD with exact congruence and coprimality checks\"}\n";g.close();cout<<"S21_FAST_PADE_CERTIFIED dimension="<<k<<" q="<<q<<" full_congruence=true coprime=true\n";
}
