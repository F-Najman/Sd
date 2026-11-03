source_genus := 11;
source_R := PolynomialRing(Rationals(),11);
source_equations := [source_R |
(-1)*source_R.1*source_R.2+(1)*source_R.2*source_R.5+(-1)*source_R.5*source_R.8,
(1)*source_R.2*source_R.10+(-1)*source_R.3*source_R.7+(-1)*source_R.3*source_R.11,
(-1)*source_R.2*source_R.5+(-1)*source_R.2*source_R.10+(1)*source_R.3*source_R.4+(1)*source_R.3*source_R.6,
(1)*source_R.1*source_R.2+(-1)*source_R.1*source_R.3+(1)*source_R.2*source_R.3+(-1)*source_R.3*source_R.4,
(-1)*source_R.1*source_R.9+(1)*source_R.3*source_R.4+(-1)*source_R.3*source_R.8+(1)*source_R.3*source_R.11,
(-1)*source_R.1*source_R.8+(1)*source_R.1*source_R.9+(-1)*source_R.2*source_R.3+(-1)*source_R.2*source_R.10,
(1)*source_R.1*source_R.2+(-1)*source_R.1*source_R.5+(-1)*source_R.1*source_R.9+(1)*source_R.2*source_R.3+(1)*source_R.2*source_R.11,
(1)*source_R.1*source_R.9+(-1)*source_R.2*source_R.3+(-1)*source_R.2*source_R.5+(1)*source_R.3*source_R.5+(1)*source_R.5*source_R.6,
(1)*source_R.2*source_R.7+(-1)*source_R.2*source_R.10+(1)*source_R.3*source_R.6+(1)*source_R.3*source_R.8+(1)*source_R.4*source_R.8+(1)*source_R.9*source_R.10,
(1)*source_R.1*source_R.5+(1)*source_R.2*source_R.3+(-1)*source_R.3*source_R.8+(-1)*source_R.5*source_R.8+(-1)*source_R.8*source_R.11+(-1)*source_R.9*source_R.10,
(-1)*source_R.1*source_R.1+(-1)*source_R.1*source_R.2+(1)*source_R.1*source_R.6+(1)*source_R.3*source_R.6+(1)*source_R.3*source_R.8+(1)*source_R.9*source_R.10,
(-1)*source_R.1*source_R.8+(-1)*source_R.2*source_R.2+(1)*source_R.2*source_R.4+(1)*source_R.2*source_R.5+(-1)*source_R.3*source_R.4+(1)*source_R.3*source_R.8+(1)*source_R.9*source_R.10,
(1)*source_R.1*source_R.9+(1)*source_R.2*source_R.5+(1)*source_R.5*source_R.7+(-1)*source_R.5*source_R.10,
(1)*source_R.1*source_R.1+(1)*source_R.1*source_R.4+(-1)*source_R.1*source_R.5+(-1)*source_R.2*source_R.5+(-1)*source_R.5*source_R.7,
(-1)*source_R.1*source_R.5+(1)*source_R.2*source_R.10+(-1)*source_R.3*source_R.5+(1)*source_R.5*source_R.8+(-1)*source_R.5*source_R.10+(1)*source_R.9*source_R.11,
(-1)*source_R.2*source_R.6+(1)*source_R.2*source_R.7+(1)*source_R.2*source_R.9+(-1)*source_R.3*source_R.5+(1)*source_R.5*source_R.8,
(1)*source_R.2*source_R.2+(1)*source_R.2*source_R.7+(1)*source_R.2*source_R.9+(-1)*source_R.2*source_R.10+(-1)*source_R.8*source_R.9,
(-1)*source_R.1*source_R.1+(1)*source_R.1*source_R.7+(-1)*source_R.1*source_R.10+(1)*source_R.2*source_R.5+(1)*source_R.2*source_R.10+(1)*source_R.9*source_R.10,
(1)*source_R.1*source_R.2+(-1)*source_R.1*source_R.3+(-1)*source_R.1*source_R.5+(-1)*source_R.1*source_R.10+(-1)*source_R.2*source_R.4+(-1)*source_R.2*source_R.7+(1)*source_R.6*source_R.10,
(1)*source_R.2*source_R.3+(1)*source_R.2*source_R.10+(-1)*source_R.3*source_R.4+(1)*source_R.5*source_R.6+(-1)*source_R.6*source_R.8+(1)*source_R.7*source_R.8+(1)*source_R.8*source_R.9,
(-1)*source_R.1*source_R.7+(-1)*source_R.1*source_R.9+(1)*source_R.2*source_R.3+(-1)*source_R.2*source_R.9+(1)*source_R.4*source_R.9+(-1)*source_R.6*source_R.11,
(1)*source_R.1*source_R.9+(-1)*source_R.2*source_R.4+(1)*source_R.2*source_R.8+(-1)*source_R.2*source_R.9+(-1)*source_R.2*source_R.11+(1)*source_R.4*source_R.9,
(-1)*source_R.1*source_R.2+(1)*source_R.1*source_R.3+(1)*source_R.2*source_R.2+(-1)*source_R.2*source_R.8+(1)*source_R.3*source_R.3+(1)*source_R.3*source_R.6+(-1)*source_R.3*source_R.11+(1)*source_R.8*source_R.10,
(-1)*source_R.1*source_R.5+(-1)*source_R.1*source_R.7+(-1)*source_R.2*source_R.3+(-1)*source_R.3*source_R.6+(-1)*source_R.7*source_R.11+(-1)*source_R.8*source_R.10+(-1)*source_R.9*source_R.10+(1)*source_R.10*source_R.11,
(-1)*source_R.1*source_R.5+(1)*source_R.2*source_R.10+(-1)*source_R.3*source_R.5+(-1)*source_R.3*source_R.6+(1)*source_R.3*source_R.9+(1)*source_R.5*source_R.5+(1)*source_R.5*source_R.10,
(-1)*source_R.1*source_R.5+(-1)*source_R.1*source_R.10+(1)*source_R.3*source_R.7+(1)*source_R.3*source_R.8+(1)*source_R.3*source_R.9+(1)*source_R.5*source_R.6+(-1)*source_R.6*source_R.6+(1)*source_R.6*source_R.7+(1)*source_R.6*source_R.9+(1)*source_R.9*source_R.10,
(-1)*source_R.1*source_R.3+(1)*source_R.1*source_R.6+(1)*source_R.1*source_R.9+(-1)*source_R.2*source_R.4+(1)*source_R.3*source_R.9+(1)*source_R.4*source_R.6+(-1)*source_R.4*source_R.8+(1)*source_R.6*source_R.9+(-1)*source_R.8*source_R.9,
(-1)*source_R.1*source_R.1+(1)*source_R.1*source_R.3+(-1)*source_R.1*source_R.8+(1)*source_R.2*source_R.6+(-1)*source_R.4*source_R.6+(1)*source_R.4*source_R.8+(-1)*source_R.8*source_R.8,
(-1)*source_R.1*source_R.10+(1)*source_R.2*source_R.2+(1)*source_R.3*source_R.4+(-1)*source_R.3*source_R.8+(1)*source_R.4*source_R.6+(-1)*source_R.5*source_R.10+(-1)*source_R.6*source_R.11+(1)*source_R.7*source_R.9+(1)*source_R.9*source_R.11,
(-1)*source_R.1*source_R.1+(-1)*source_R.1*source_R.11+(1)*source_R.2*source_R.5+(1)*source_R.4*source_R.10+(1)*source_R.9*source_R.10,
(-1)*source_R.1*source_R.5+(1)*source_R.1*source_R.9+(-1)*source_R.3*source_R.5+(-1)*source_R.4*source_R.6+(1)*source_R.4*source_R.7+(1)*source_R.4*source_R.9+(-1)*source_R.4*source_R.10+(-1)*source_R.9*source_R.10,
(-1)*source_R.1*source_R.2+(1)*source_R.1*source_R.10+(1)*source_R.3*source_R.11+(1)*source_R.4*source_R.5+(1)*source_R.4*source_R.10+(-1)*source_R.5*source_R.10+(1)*source_R.9*source_R.10,
(-1)*source_R.1*source_R.1+(-1)*source_R.1*source_R.6+(1)*source_R.2*source_R.3+(1)*source_R.2*source_R.4+(1)*source_R.3*source_R.7+(-1)*source_R.4*source_R.4+(1)*source_R.8*source_R.10+(-1)*source_R.10*source_R.11,
(-1)*source_R.1*source_R.6+(1)*source_R.1*source_R.7+(1)*source_R.1*source_R.11+(1)*source_R.2*source_R.3+(-1)*source_R.2*source_R.4+(1)*source_R.2*source_R.5+(-1)*source_R.2*source_R.9+(1)*source_R.2*source_R.11+(1)*source_R.4*source_R.4+(1)*source_R.4*source_R.9+(-1)*source_R.5*source_R.11,
(-1)*source_R.4*source_R.10+(1)*source_R.5*source_R.7+(1)*source_R.5*source_R.11+(-1)*source_R.6*source_R.10+(1)*source_R.7*source_R.10+(1)*source_R.10*source_R.11,
(1)*source_R.1*source_R.1+(1)*source_R.1*source_R.2+(-1)*source_R.1*source_R.4+(1)*source_R.1*source_R.6+(-1)*source_R.3*source_R.4+(1)*source_R.5*source_R.6+(1)*source_R.6*source_R.7+(-1)*source_R.7*source_R.7+(-1)*source_R.7*source_R.9
];
source_cusp := [Rationals() | 0,0,0,0,0,0,0,0,-1,0,0];
target_genus := 5;
target_R := PolynomialRing(Rationals(),5);
target_equations := [target_R |
(-1)*target_R.1*target_R.2+(1)*target_R.1*target_R.3+(1)*target_R.2*target_R.5,
(1)*target_R.1*target_R.1+(1)*target_R.2*target_R.2+(-1)*target_R.3*target_R.4+(1)*target_R.4*target_R.4+(-1)*target_R.4*target_R.5,
(1)*target_R.1*target_R.2+(1)*target_R.1*target_R.3+(-1)*target_R.1*target_R.5+(-1)*target_R.2*target_R.3+(1)*target_R.2*target_R.5+(1)*target_R.3*target_R.5,
(-1)*target_R.1*target_R.2*target_R.2+(1)*target_R.1*target_R.2*target_R.3+(1)*target_R.2*target_R.2*target_R.5,
(-1)*target_R.1*target_R.2*target_R.3+(1)*target_R.1*target_R.3*target_R.3+(1)*target_R.2*target_R.3*target_R.5,
(-1)*target_R.1*target_R.1*target_R.2+(1)*target_R.1*target_R.1*target_R.3+(1)*target_R.1*target_R.2*target_R.5,
(-1)*target_R.1*target_R.2*target_R.5+(1)*target_R.1*target_R.3*target_R.5+(1)*target_R.2*target_R.5*target_R.5,
(-1)*target_R.1*target_R.2*target_R.4+(1)*target_R.1*target_R.3*target_R.4+(1)*target_R.2*target_R.4*target_R.5,
(1)*target_R.1*target_R.1*target_R.2+(1)*target_R.2*target_R.2*target_R.2+(-1)*target_R.2*target_R.3*target_R.4+(1)*target_R.2*target_R.4*target_R.4+(-1)*target_R.2*target_R.4*target_R.5,
(1)*target_R.1*target_R.1*target_R.5+(1)*target_R.2*target_R.2*target_R.5+(-1)*target_R.3*target_R.4*target_R.5+(1)*target_R.4*target_R.4*target_R.5+(-1)*target_R.4*target_R.5*target_R.5,
(-1)*target_R.1*target_R.1*target_R.2+(-1)*target_R.1*target_R.1*target_R.3+(1)*target_R.1*target_R.1*target_R.5+(1)*target_R.1*target_R.2*target_R.3+(-1)*target_R.1*target_R.2*target_R.5+(-1)*target_R.1*target_R.3*target_R.5,
(-1)*target_R.1*target_R.2*target_R.3+(-1)*target_R.1*target_R.3*target_R.3+(1)*target_R.1*target_R.3*target_R.5+(1)*target_R.2*target_R.3*target_R.3+(-1)*target_R.2*target_R.3*target_R.5+(-1)*target_R.3*target_R.3*target_R.5,
(-1)*target_R.1*target_R.1*target_R.2+(1)*target_R.1*target_R.1*target_R.3+(-1)*target_R.1*target_R.2*target_R.5+(1)*target_R.1*target_R.5*target_R.5+(1)*target_R.2*target_R.3*target_R.5+(-1)*target_R.3*target_R.5*target_R.5,
(-1)*target_R.1*target_R.2*target_R.2+(-1)*target_R.1*target_R.2*target_R.3+(1)*target_R.1*target_R.2*target_R.5+(1)*target_R.2*target_R.2*target_R.3+(-1)*target_R.2*target_R.2*target_R.5+(-1)*target_R.2*target_R.3*target_R.5,
(1)*target_R.1*target_R.1*target_R.3+(1)*target_R.2*target_R.2*target_R.3+(-1)*target_R.3*target_R.3*target_R.4+(1)*target_R.3*target_R.4*target_R.4+(-1)*target_R.3*target_R.4*target_R.5,
(1)*target_R.1*target_R.1*target_R.1+(1)*target_R.1*target_R.2*target_R.2+(-1)*target_R.1*target_R.3*target_R.4+(1)*target_R.1*target_R.4*target_R.4+(-1)*target_R.1*target_R.4*target_R.5,
(1)*target_R.1*target_R.1*target_R.4+(1)*target_R.2*target_R.2*target_R.4+(-1)*target_R.3*target_R.4*target_R.4+(1)*target_R.4*target_R.4*target_R.4+(-1)*target_R.4*target_R.4*target_R.5,
(1)*target_R.1*target_R.2*target_R.4+(1)*target_R.1*target_R.3*target_R.4+(-1)*target_R.1*target_R.4*target_R.5+(-1)*target_R.2*target_R.3*target_R.4+(1)*target_R.2*target_R.4*target_R.5+(1)*target_R.3*target_R.4*target_R.5
];
target_cusp := [Rationals() | 0,0,1,1,0];
N := 65;
cover_degree := 2;
L := Matrix(Rationals(),5,11,[-1,1,-1,-1,0,0,0,0,0,0,0,0,1,0,0,-1,0,0,-1,0,0,0,0,1,-1,-1,0,-1,0,0,-1,0,0,0,0,0,0,-1,1,-2,-1,-1,0,0,0,1,0,0,-1,0,0,-1,0,-1,1]);
precision := 54;
target_basis := Matrix(Rationals(),5,53,[0,0,-1,1,0,1,1,-1,-1,-1,1,-1,0,-1,0,0,2,1,1,1,-2,-3,1,1,0,1,2,3,-3,0,-3,-2,1,0,1,-2,-3,-1,0,0,0,4,-1,3,1,1,-1,1,4,0,2,-1,0,0,-1,0,1,0,0,1,0,1,0,0,0,0,-3,-1,0,0,0,-2,1,0,0,0,2,0,0,2,3,-1,1,0,1,-3,0,1,0,-3,0,1,-1,2,2,-4,2,-1,-2,-1,-4,4,-1,0,-1,6,1,0,0,1,0,0,2,-2,-1,-1,0,-2,0,-2,0,-1,0,-2,2,0,-2,-2,2,2,1,1,2,6,-4,2,4,0,-2,2,0,-1,-2,4,0,-1,-4,2,2,2,0,2,2,0,1,0,-4,0,-6,1,-1,-1,0,0,2,-1,0,0,0,2,-1,-1,-1,1,1,0,0,-2,1,2,-3,-3,-2,1,1,2,7,1,0,-2,-1,-3,-2,3,-1,-1,3,1,-3,-6,0,3,2,-1,2,1,1,7,-1,-4,0,-2,0,-1,0,0,1,2,0,-1,0,0,2,-2,-1,-4,0,4,-2,3,0,1,-2,-2,-2,0,0,0,-2,4,4,0,2,3,0,-4,2,0,2,-4,0,-2,-2,6,-6,4,-1,-4,-4,0,4,-1,0,-1,0]);
