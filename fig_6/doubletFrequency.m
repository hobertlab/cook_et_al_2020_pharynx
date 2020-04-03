function [doubletCounts doubletCountsRand] = doubletFrequency(obj,varargin)
%DOUBLETFREQUENCY Count frequency of doublet motifs in AdjacencyMatrix
%object


tolerance = 5;
nIters = 1000;
moduleAnalysis = false;
for i = 1:2:numel(varargin)
    switch varargin{i}
        case 'threshold'
            tolerance = varargin{i+1};
        case 'nIters'
            nIters = varargin{i+1};
        case 'moduleAnalysis'
            moduleAnalysis = varargin{i+1};
    end
end

[Aorig labelsOrig] = getSquareMatrix(obj);
Aorig(logical(eye(size(Aorig)))) = 0;   %clear self-loops
labels = labelsOrig;
A = double(Aorig>=tolerance);

doubletCounts = full(AdjacencyMatrix.countDoublets(A));
fprintf('\nDoublet Analysis:\n');
for jj = 1:3, fprintf('Count of motif %u: %u\n',jj, doubletCounts(jj)); end

if moduleAnalysis

    [commLabels Q reducedMat] = getCommunitiesMM(obj,'quiet');
    labels = createList(commLabels,'');
    % Get reordered matrix
    [tmp A] = getSubMatrix(obj,labels, labels');
    A = double(A>=tolerance);
    modulesMat = zeros(size(A));
    idx = 1;
    for kk = 1:numel(commLabels)
        modulesMat(idx:(idx+numel(commLabels{kk}) - 1),idx:(idx+numel(commLabels{kk})) - 1) = 1;
        idx = idx+numel(commLabels{kk});
    end
    modulesMat = logical(modulesMat);
    countsInModule = full(AdjacencyMatrix.countDoublets(A & modulesMat));
    countsBetwModule = full(AdjacencyMatrix.countDoublets(A & ~modulesMat));
    for jj = 2:3, fprintf('Count of motif %u in modules: %u\n',jj, countsInModule(jj)); end
    for jj = 2:3, fprintf('Count of motif %u between modules: %u\n',jj, countsBetwModule(jj)); end
   
end

% Initialize random doublet counts matrix
doubletCountsRand = zeros(nIters,3);

for i = 1:nIters
    %     Arand = randmio_dir(A,20);
    Arand = randmio_dir(Aorig,20);
    Arand = double(Arand>=tolerance);
    doubletCountsRand(i,:) = AdjacencyMatrix.countDoublets(Arand);


end

fprintf('\n');
for jj = 1:3, fprintf('Average count of motif %u, randomly rewired: %f\n',jj, mean(doubletCountsRand(:,jj))); end

if moduleAnalysis
    
    nItersModule = 200;
    countsInModuleRand = zeros(nItersModule,3);
    countsBetwModuleRand = zeros(nItersModule,3);
    
    for i = 1:nItersModule
        Arand = rand_doubletcons_bin(double(Aorig>=tolerance),10);
        
        %Now test statistical significance
        adjMatRand = AdjacencyMatrix(Arand,labelsOrig,labelsOrig');
        
        [commLabels Q] = getCommunitiesMM(adjMatRand,'quiet');
        labelsRand = createList(commLabels,'');
        % Get reordered matrix
        [tmp Arand] = getSubMatrix(adjMatRand,labelsRand,labelsRand');
%         Arand = (Arand>=tolerance);
%         AdjacencyMatrix.countDoublets(Arand)
        modulesMat = zeros(size(Arand));
        idx = 1;
        for kk = 1:numel(commLabels)
            modulesMat(idx:(idx+numel(commLabels{kk}) - 1),idx:(idx+numel(commLabels{kk})) - 1) = 1;
            idx = idx+numel(commLabels{kk});
        end
        modulesMat = logical(modulesMat);
        countsInModuleRand(i,:) = full(AdjacencyMatrix.countDoublets(Arand & modulesMat));
        countsBetwModuleRand(i,:) = full(AdjacencyMatrix.countDoublets(Arand & ~modulesMat));
        
    end
    
    for jj = 2:3, fprintf('Average Count of motif %u in modules, randomly rewired, conserving doublets: %f\n',jj, mean(countsInModuleRand(:,jj))); end
    for jj = 2:3, fprintf('Average Count of motif %u between modules, randomly rewired, conserving doublets: %f\n',jj, mean(countsBetwModuleRand(:,jj))); end

end


figure;
hold on;
for i = 1:nIters
    scatter(1:3,doubletCountsRand(i,:)./mean(doubletCountsRand,1),'r+');
end
scatter(1:3,doubletCounts./mean(doubletCountsRand,1),'bs','MarkerFaceColor','b');
xlim([1,3]);
ylim([0,20]);
grid on
set(gca,'XTick',1:3);
set(gca,'YScale','log');

title('Ratio of Doublet Counts to Expected Doublet Counts');


end


