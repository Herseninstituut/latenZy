function ind = my_randperm(n, k, seed)
% deterministic random permutation for MATLAB/Python consistency
%
% usage:
%   ind = my_randperm(n)
%   ind = my_randperm(n, k)
%   ind = my_randperm(n, k, seed)
%
% parameters:
%   n    - upper bound for permutation (0-indexed in Python, 1-indexed in MATLAB)
%   k    - number of elements to return (default: n)
%   seed - random seed for reproducibility (default: 1)
%
% returns:
%   ind  - random permutation indices (1-based in MATLAB)
%
% examples:
%   my_randperm(5)
%   my_randperm(10, 3)
%   my_randperm(10, [], 42)

if nargin < 3 || isempty(seed)
    seed = 1;
end
if nargin < 2 || isempty(k)
    k = n;
end

rng(seed);  %set deterministic seed
[~, ind] = sort(rand(1, n));
ind = ind(1:k);
end
