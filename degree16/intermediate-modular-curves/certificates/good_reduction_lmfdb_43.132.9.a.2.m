
// Modular curves downloaded from the LMFDB on 12 July 2026.
// Magma code for modular curve with label 43.132.9.a.2

// Other names and/or labels
// Cummins-Pauli label: 43A9
// Rouse-Sutherland-Zureick-Brown label: 43.132.9.1
// Sutherland label: 43B.2.1

// Group data
level := 43;
// Elements that, together with Gamma(level), generate the group
gens := [[21, 6, 0, 8], [42, 15, 0, 12]];
// Group contains -1?
ContainsMinus1 := true;
// Index in Gamma(1)
index := 132;

// Curve data
conductor := [[43, 9]];
bad_primes := [43];
// Genus
g := 9;
// Rank
r := 1
;// Exact gonality known

// Modular data
// Number of cusps
Ncusps := 6
;// Number of rational cusps
Nrat_cusps := 3
;// CM discriminants
CM_discs := [];
// Groups containing given group, corresponding to curves covered by given curve
covers := ["43.44.3.a.1"];

// Models for this modular curve, if computed
Pol<x,y,z,w,t,u,v,r,s> := PolynomialRing(Rationals(), 9);
// Isomorphic to P^1?
is_P1 := false;

// Canonical model
model_0 := [y^2-y*u+y*s+w^2-w*u+w*s-t*s+u*v-u*s-v^2-v*r,x^2-x*u-y^2+y*z+y*u-y*v-y*s-w^2+w*t+w*u-w*v,x^2-x*y-x*v+y*z+y*t-y*v+y*s-z*s-w^2+w*u+t*s-u*s+2*v*r-r*s,x*v-x*s-y*v+y*s+z*v-z*s+w*v+t*s+u*v-u*s-v^2+v*r-r*s,x*v-y*t+w*t-w*v-w*s-2*t*r-t*s+u*v+u*s-v^2-v*s+2*r*s,x*y-x*w+x*r-y^2+y*u-y*v-y*r-y*s+z*v+w^2-w*u+w*v-w*r+t*r-2*v*r,x*v-x*s-y^2+y*w-y*t-y*r-y*s-w^2+w*t+w*r-t*r+u^2-u*v+u*r-v*r,x*w-x*u-y*z+y*w+y*t-y*v-z*v-w*u+w*r+u^2-u*v-v*r-v*s,x*z-x*w+x*s-y*z-y*s+z^2+2*z*w+z*s-w*t+w*v+2*t*r+t*s+u*s-v*r-v*s,x^2-x*y+x*w-x*v+x*r+y*t-y*r-z*s+w^2-w*u-t*r+u^2-2*u*v-u*s+v^2+v*r+v*s-r*s,x*y-x*w-x*u+x*v+x*s+y*w-y*u+y*s-z*s-w^2+w*t-w*s-t*r+u^2-u*v-v*s+r*s,x*z-x*t+2*x*s-y*z-y*w+y*t+z*w-z*s-w*t+w*u-w*r-t*u+t*v+t*r+t*s-u*v-u*s+v^2+v*r+v*s-r*s,x*s+y*t+y*v-y*s-2*w*v-t*u+t*v-t*r+v*r+v*s,x*v-x*s+y*v+w*t-w*s-t*u+t*v-t*r+t*s+u*s+v*r,x^2-x*y-x*w+x*u-x*v+x*s+z^2+z*w+z*v-z*r-w*r+v*r,x^2-x*u+x*v-y*t+y*v+y*r-y*s+z^2+z*u+z*s+w*t-u*r+u*s,x*y-x*z-x*u+y*z+y*t-y*v+y*s-z^2-z*w+z*t-z*s-u*s-v*r,x*z-x*t+x*v+x*r+x*s-y*t-y*r+z*v+z*r+w^2-w*u+w*v-t*r-t*s-v*r+r*s,x*w-x*v-y^2-2*y*t+y*u+y*v-y*s-z*w+z*v+w*t-t^2-t*s-u*v+v^2-v*r+v*s,x*v+x*s-y*t+z*w+z*t-z*v+z*s+w*v-t*r+u*s+v*r-v*s+r*s,x*w-x*s-y*s-z*t-z*v+z*s-w*t-w*u+2*w*v+w*s+t*s-r*s];

// Singular plane model
model_1 := [4*x^12*y^2+86*x^11*y^3+563*x^10*y^4-23*x^9*y^5+11*x^8*y^6+5*x^7*y^7+2*x^6*y^8-14*x^11*y^2*z-278*x^10*y^3*z-3435*x^9*y^4*z+109*x^8*y^5*z-53*x^7*y^6*z-25*x^6*y^7*z-12*x^5*y^8*z-45*x^10*y^2*z^2-835*x^9*y^3*z^2+9290*x^8*y^4*z^2-189*x^7*y^5*z^2+78*x^6*y^6*z^2+57*x^5*y^7*z^2+30*x^4*y^8*z^2+8*x^10*y*z^3+331*x^9*y^2*z^3+4866*x^8*y^3*z^3-14557*x^7*y^4*z^3+70*x^6*y^5*z^3+21*x^5*y^6*z^3-85*x^4*y^7*z^3-40*x^3*y^8*z^3-4*x^9*y*z^4+246*x^8*y^2*z^4-9794*x^7*y^3*z^4+14794*x^6*y^4*z^4+154*x^5*y^5*z^4-188*x^4*y^6*z^4+95*x^3*y^7*z^4+30*x^2*y^8*z^4-122*x^8*y*z^5-2370*x^7*y^2*z^5+11411*x^6*y^3*z^5-10506*x^5*y^4*z^5-109*x^4*y^5*z^5+217*x^3*y^6*z^5-75*x^2*y^7*z^5-12*x*y^8*z^5+4*x^8*z^6-16*x^7*y*z^6+3909*x^6*y^2*z^6-8536*x^5*y^3*z^6+5444*x^4*y^4*z^6-121*x^3*y^5*z^6-98*x^2*y^6*z^6+35*x*y^7*z^6+2*y^8*z^6+14*x^7*z^7+489*x^6*y*z^7-3202*x^5*y^2*z^7+4059*x^4*y^3*z^7-1979*x^3*y^4*z^7+160*x^2*y^5*z^7+7*x*y^6*z^7-7*y^7*z^7-3*x^6*z^8-660*x^5*y*z^8+1553*x^4*y^2*z^8-1152*x^3*y^3*z^8+421*x^2*y^4*z^8-53*x*y^5*z^8+5*y^6*z^8-38*x^5*z^9+385*x^4*y*z^9-474*x^3*y^2*z^9+187*x^2*y^3*z^9-35*x*y^4*z^9+2*y^5*z^9+40*x^4*z^10-105*x^3*y*z^10+83*x^2*y^2*z^10-20*x*y^3*z^10+2*y^4*z^10-15*x^3*z^11+10*x^2*y*z^11-4*x*y^2*z^11+2*x^2*z^12];

// Maps from this modular curve, if computed

// Map from the canonical model to the canonical model of modular curve with label 43.44.3.a.1
//   Coordinate number 0:
map_0_coord_0 := 1*(-y+z-t);
//   Coordinate number 1:
map_0_coord_1 := 1*(-x-y-2*w+t+3*u-3*v);
//   Coordinate number 2:
map_0_coord_2 := 1*(-x-w+t+u-r+s);
// Codomain equation:
map_0_codomain := [4*x^4-3*x^3*y+2*x^2*y^2-x*y^3+3*x^3*z+x*y^2*z+y^3*z+2*x^2*z^2-x*y*z^2-y^2*z^2+x*z^3+y*z^3];

// Map from the canonical model to the plane model of modular curve with label 43.132.9.a.2
//   Coordinate number 0:
map_1_coord_0 := 1*(v);
//   Coordinate number 1:
map_1_coord_1 := 1*(r);
//   Coordinate number 2:
map_1_coord_2 := 1*(s);
// Codomain equation:
map_1_codomain := [4*x^12*y^2+86*x^11*y^3+563*x^10*y^4-23*x^9*y^5+11*x^8*y^6+5*x^7*y^7+2*x^6*y^8-14*x^11*y^2*z-278*x^10*y^3*z-3435*x^9*y^4*z+109*x^8*y^5*z-53*x^7*y^6*z-25*x^6*y^7*z-12*x^5*y^8*z-45*x^10*y^2*z^2-835*x^9*y^3*z^2+9290*x^8*y^4*z^2-189*x^7*y^5*z^2+78*x^6*y^6*z^2+57*x^5*y^7*z^2+30*x^4*y^8*z^2+8*x^10*y*z^3+331*x^9*y^2*z^3+4866*x^8*y^3*z^3-14557*x^7*y^4*z^3+70*x^6*y^5*z^3+21*x^5*y^6*z^3-85*x^4*y^7*z^3-40*x^3*y^8*z^3-4*x^9*y*z^4+246*x^8*y^2*z^4-9794*x^7*y^3*z^4+14794*x^6*y^4*z^4+154*x^5*y^5*z^4-188*x^4*y^6*z^4+95*x^3*y^7*z^4+30*x^2*y^8*z^4-122*x^8*y*z^5-2370*x^7*y^2*z^5+11411*x^6*y^3*z^5-10506*x^5*y^4*z^5-109*x^4*y^5*z^5+217*x^3*y^6*z^5-75*x^2*y^7*z^5-12*x*y^8*z^5+4*x^8*z^6-16*x^7*y*z^6+3909*x^6*y^2*z^6-8536*x^5*y^3*z^6+5444*x^4*y^4*z^6-121*x^3*y^5*z^6-98*x^2*y^6*z^6+35*x*y^7*z^6+2*y^8*z^6+14*x^7*z^7+489*x^6*y*z^7-3202*x^5*y^2*z^7+4059*x^4*y^3*z^7-1979*x^3*y^4*z^7+160*x^2*y^5*z^7+7*x*y^6*z^7-7*y^7*z^7-3*x^6*z^8-660*x^5*y*z^8+1553*x^4*y^2*z^8-1152*x^3*y^3*z^8+421*x^2*y^4*z^8-53*x*y^5*z^8+5*y^6*z^8-38*x^5*z^9+385*x^4*y*z^9-474*x^3*y^2*z^9+187*x^2*y^3*z^9-35*x*y^4*z^9+2*y^5*z^9+40*x^4*z^10-105*x^3*y*z^10+83*x^2*y^2*z^10-20*x*y^3*z^10+2*y^4*z^10-15*x^3*z^11+10*x^2*y*z^11-4*x*y^2*z^11+2*x^2*z^12];
