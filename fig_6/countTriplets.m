function tripletcount = countTriplets(A)
% clear self loops
A(logical(eye(size(A)))) = 0;

% Chklovskii method
D = (1-A).*(1-A)'; D = D - D.*eye(size(D)); % not Aij and not Aji
U = A.*(1-A)';  %Aij and not Aji
B = A.*A'; % Aij and Aji

tripletcount(1) = 1/6*sum(sum(D.*(D^2)));
tripletcount(2) = sum(sum(U.*(D^2)));
tripletcount(3) = 1/2*sum(sum(B.*(D^2)));
tripletcount(4) = 1/2*sum(sum(D.*(U'*U)));
tripletcount(5) = 1/2*sum(sum(D.*(U*U')));
tripletcount(6) = sum(sum(D.*(U^2)));
tripletcount(7) = sum(sum(D.*(U*B)));
tripletcount(8) = sum(sum(D.*(U'*B)));
tripletcount(9) = 1/2*sum(sum(D.*(B^2)));
tripletcount(10) = sum(sum(U.*(U^2)));  % = sum(diag(U^2*U'));

tripletcount(11) = 1/3*sum(sum(U'.*(U^2)));
tripletcount(12) = 1/2*sum(sum(B.*(U'*U)));
tripletcount(13) = sum(sum(B.*(U^2)));
tripletcount(14) = 1/2*sum(sum(B.*(U*U')));
tripletcount(15) = sum(sum(U.*(B^2)));
tripletcount(16) = 1/6*sum(sum(B.*(B^2)));
end