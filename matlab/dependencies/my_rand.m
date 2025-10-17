function r = my_rand(varargin)
% deterministic uniform random numbers compatible with Python my_rand
%
% usage:
%   r = my_rand()
%   r = my_rand(n)
%   r = my_rand(m, n, ...)
%   r = my_rand(..., 'seed', 42)
%
% notes:
% - my_rand(n) -> n x n matrix
% - my_rand(m, n, ...) -> m x n matrix
% - Default seed ensures reproducibility

%default seed
seed = 1;

%check for seed argument
seedIdx = find(strcmp(varargin, 'seed'), 1);
if ~isempty(seedIdx)
    seed = varargin{seedIdx+1};
    varargin([seedIdx seedIdx+1]) = [];  % remove seed from size args
end

rng(seed);  %set deterministic seed

%determine output size
if isempty(varargin)
    sz = [1 1];
elseif isscalar(varargin)
    sz = [varargin{1} varargin{1}]; %MATLAB behavior like Python
else
    sz = cell2mat(varargin);
end

numel_out = prod(sz);

%generate deterministic random values via permutation trick
[~, perm] = sort(rand(1, numel_out));
r = (perm - 1) / numel_out;

%reshape to desired size
r = reshape(r, sz);
end
