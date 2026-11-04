#include <iostream>
#include <array>
#include <cstdint>
#include <numeric>
#include <cstdlib>
using namespace std;
// Q8: 0=1, 1=-1, 2=i,3=-i,4=j,5=-j,6=k,7=-k
int mul(int a,int b){
  int sa=a%2 ? -1:1, sb=b%2 ? -1:1;
  int ax=a/2, bx=b/2, out=0, sign=sa*sb;
  if(ax==0) out=bx;
  else if(bx==0) out=ax;
  else if(ax==bx){out=0;sign=-sign;}
  else {out=6-ax-bx; if((ax==1&&bx==3)||(ax==2&&bx==1)||(ax==3&&bx==2))sign=-sign;}
  return out*2+(sign<0);
}
int inv(int a){return a<2?a:(a^1);}
int weight(int a,int sign){if(a==0)return 17+2*sign; if(a==1)return 17-2*sign; return 5;}
int trace2(int a){if(a==0)return 2;if(a==1)return -2;return 0;}
// orientation: site(x,t), x=0..2, t=0,1, U for x direction, V temporal
int main(){
   for(int a=0;a<8;a++)for(int b=0;b<8;b++)for(int c=0;c<8;c++)if(mul(mul(a,b),c)!=mul(a,mul(b,c))){cerr<<"group associativity FAIL"<<endl;return 2;}
   for(int a=0;a<8;a++)if(mul(a,inv(a))!=0 || mul(inv(a),a)!=0){cerr<<"group inverse FAIL"<<endl;return 2;}
   int U[2][3]={{0,0,0},{0,0,0}};
   int V[2][3]={{0,0,0},{0,0,0}};
   // fix U[0][0],U[0][1],U[1][0],U[1][1], V[0][0] to 1; free U[0][2],U[1][2], V[0][1],V[0][2],V[1][0..2]
   long long sums[2]={0,0},grams[2]={0,0};
   for(int a=0;a<8;a++)for(int b=0;b<8;b++)for(int c=0;c<8;c++)for(int d=0;d<8;d++)for(int e=0;e<8;e++)for(int f=0;f<8;f++)for(int g=0;g<8;g++){
      U[0][2]=a; U[1][2]=b; V[0][1]=c;V[0][2]=d;V[1][0]=e;V[1][1]=f;V[1][2]=g;
      int plaquettes[6]; int p=0;
      for(int t=0;t<2;t++)for(int x=0;x<3;x++){
         plaquettes[p++]=mul(mul(mul(U[t][x],V[t][(x+1)%3]),inv(U[(t+1)%2][x])),inv(V[t][x]));
      }
      long long trprod=trace2(a)*trace2(b);
      for(int z=0;z<2;z++){
          int sign=z? -1:1;
          long long w=1;
          for(int j=0;j<6;j++)w*=weight(plaquettes[j],sign);
          sums[z]+=w;
          grams[z]+=w*trprod;
      }
   }
   const long long denom = 1LL<<21;
   if(grams[0]*4 != 593*denom || grams[1]*4 != -593*denom || sums[0] != sums[1]){
       cerr << "Q8_GRAM|status=FAIL|json=0\n"; return 2;
   }
   for(int z=0;z<2;z++){
       long long dg=std::gcd(std::llabs(grams[z]),denom);
       long long dz=std::gcd(sums[z],denom);
       cout<<"Q8_GRAM|c_two="<<(z?"-1":"+1")<<"|assignments="<<denom
           <<"|Gram="<<(grams[z]/dg)<<"/"<<(denom/dg)
           <<"|Z="<<(sums[z]/dz)<<"/"<<(denom/dz)
           <<"|status=PASS|json=0\n";
   }
}
