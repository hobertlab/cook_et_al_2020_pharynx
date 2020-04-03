function doubletCounts = countDoublets(A)

% Clear self loops
A(logical(eye(size(A)))) = 0;

doubletCounts(1) = sum(sum(~(A | A')));
doubletCounts(2) = sum(sum(A & ~(A')));
doubletCounts(3) = .5 * sum(sum(A & A'));

end

