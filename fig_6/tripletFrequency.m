function [tripletCounts tripletCountsRand] = tripletFrequency( obj,varargin)
%TRIPLETMOTIFS Count triplet motifs in AdjacencyMatrix obj
%    tripletMotifs(obj) will plot the significance for
%    frequency of occurence in AdjacencyMatrix obj, compared to the null
%    model of a randomly rewired matrix.  The 16 specific triplets can be
%    found in Varshney, Chen, Paniagua, Hall, Chklovskii p. 17
%
%    Optional Parameters:
%       'tolerance' - set threshold for converting weighted matrix into
%       binary matrix.  Default value is 5
%       'nIters' - set the number of iterations for performing significance
%       test.  This will determine the number of random graphs generated

tolerance = 5;
nIters = 1000;
for i = 1:2:numel(varargin)
    switch varargin{i}
        case 'tolerance'
            tolerance = varargin{i+1};
        case 'nIters'
            nIters = varargin{i+1};
    end
end

[A labels] = getSquareMatrix(obj);

A = double(A>=tolerance);

tripletCounts = AdjacencyMatrix.countTriplets(A);
fprintf('\nTriplet Analysis:\n');
for jj = 1:16, fprintf('Count of motif %u: %u\n',jj, tripletCounts(jj)); end

% Initialize random triplet counts matrix
tripletCountsRand = zeros(nIters,16);
for i = 1:nIters
    Arand = rand_doubletcons_bin(A,20); %generate random matrix, conserving doublet motifs
    tripletCountsRand(i,:) = AdjacencyMatrix.countTriplets(Arand);
end
fprintf('\n');
for jj = 1:16, fprintf('Average count of motif %u, randomly rewired: %f\n',jj, mean(tripletCountsRand(:,jj))); end

% tripletCountsRandZScores = (tripletCountsRand - repmat(mean(tripletCountsRand,1),nIters,1))./repmat(std(tripletCountsRand),nIters,1);

figure;
hold on;
for i = 1:nIters
    scatter(1:16,tripletCountsRand(i,:)./mean(tripletCountsRand,1),'r+');
end
scatter(1:16,tripletCounts./mean(tripletCountsRand,1),'bs','MarkerFaceColor','b');
xlim([1,16]);
ylim([0,20]);
grid on
set(gca,'XTick',1:16);
set(gca,'YScale','log');

title('Ratio of Triplet Counts to Expected Triplet Counts');
end


