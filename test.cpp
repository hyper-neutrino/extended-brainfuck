#include<bits/stdc++.h>
#define P std::putchar
#define G std::getchar
long long int t[30000];int p=0;int W(int x){return(x%30000+30000)%30000;}int w(int x){return((x-0)%256+256)%256+0;}int main(){t[p]=G();p=W(p+1);t[p]=G();while(t[p]){p=W(p-1);t[p]=w(t[p]+1);p=W(p+1);t[p]=w(t[p]-1);}p=W(p-1);P(t[p]);}        
