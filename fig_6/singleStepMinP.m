function Pm = singleStepMinP(M, nullData)
%SINGLESTEPMINP(M,nullData) Find statistically significant devations from
%the null hypothesis using the single step min p procedure.  Will perform
%multiple hypothesis testing on vector M compared to the null hypothesis,
%represented by vectors in nullData

if size(M,2) ~= size(nullData,2)
    error('Dimensions of M do not match dimensions of nullData');
end

nHyp = size(M,2);
nNull = size(nullData,1);
% Calculate p-values for nullData
Pik0 = zeros(size(nullData));

for kk = 1:nNull
%     for jj = 1:nHyp
%         Pik0(kk,jj) = sum(nullData(setdiff(1:nNull,kk),jj) > nullData(kk,jj)) ...
%             + .5 * sum(nullData(setdiff(1:nNull,kk),jj) == nullData(kk,jj));
%     end
        Pik0(kk,:) = sum(nullData(setdiff(1:nNull,kk),:) > repmat(nullData(kk,:),[nNull-1,1])) ...
            + .5 * sum(nullData(setdiff(1:nNull,kk),:) == repmat(nullData(kk,:),[nNull-1,1]));

end

Pik0 = Pik0./(nNull-1);

Pk0 = min(Pik0,[],2);

% Calculate p-values for given data
pi = sum(nullData > repmat(M,[nNull,1])) + .5 * sum(nullData == repmat(M,[nNull,1]));
pi = pi./nNull;
pi
% size(Pk0)
% Calculate single-step min P adjusted p-value
Pm = sum(repmat(Pk0,[1,nHyp]) <= repmat(pi,[nNull,1]));
Pm = Pm./nNull;


end

