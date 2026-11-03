small_points := [
[1,0,0,0,0,0,0],
[1,0,1,0,-1,0,-1],
[1,2,1,-2,-1,1,-2],
[1,2,1,0,-1,1,0],
[0,2,0,2,0,1,0],
[0,0,1,-1,-1,0,-1]
];

coordinate_transform := Matrix(Rationals(),7,7,[0,-1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1,0,-1,0,0,0,-1,1,1,0,1,0,-1,-1,1,0,-1,0,0,-1,1,0,0,-1]);
small_points := [Eltseq(Vector(Rationals(),v)*Transpose(coordinate_transform)):v in small_points];
