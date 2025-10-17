% test_latency_consistency.m

% Force deterministic behavior
rng(1, 'twister');

% Load example MATLAB data
data_path = fullfile(fileparts(mfilename('fullpath')), '..', 'example_data');
mat_data = load(fullfile(data_path, 'Topo2_20220126_AP.mat'));
sAP = mat_data.sAP;

% Apply inclusion criteria
clusters = sAP.sCluster;
n_clusters = length(clusters);

% Extract properties
is_good = false(n_clusters, 1);
low_contam = false(n_clusters, 1);
in_primary_visual = false(n_clusters, 1);

for i = 1:n_clusters
    is_good(i) = clusters(i).KilosortGood;
    low_contam(i) = clusters(i).Contamination < 0.1;
    
    % Handle Area field
    area_str = clusters(i).Area;
    if ischar(area_str)
        in_primary_visual(i) = contains(lower(area_str), 'primary visual');
    elseif isstring(area_str)
        in_primary_visual(i) = contains(lower(char(area_str)), 'primary visual');
    elseif iscell(area_str)
        in_primary_visual(i) = contains(lower(area_str{1}), 'primary visual');
    else
        in_primary_visual(i) = false;
    end
end

% Combine inclusion criteria
idx_incl = (is_good | low_contam) & in_primary_visual;

% Extract spike times for included clusters
spike_times_agg = cell(sum(idx_incl), 1);
counter = 1;
for i = 1:n_clusters
    if idx_incl(i)
        spike_times_agg{counter} = clusters(i).SpikeTimes;
        counter = counter + 1;
    end
end

% Get event times - Python uses [3] which is index 4 in MATLAB (1-based)
event_times = sAP.cellBlock{4}.vecStimOnTime;

% Get spike times for the 16th included cluster (Python index 15 = MATLAB index 16)
spike_times = spike_times_agg{16};

% Run latenzy with deterministic resampling
[latency, s_latenzy] = latenzy(...
    spike_times, event_times, 1, 100, 2, 0.05, true,false,false,true,1);
% 
%     'use_dur', 1, ...
%     'resamp_num', 100, ...
%     'jitter_size', 2, ...
%     'peak_alpha', 0.05, ...
%     'do_stitch', true, ...
%     'use_par_pool', false, ...
%     'use_direct_quant', false, ...
%     'restrict_neg', true, ...
%     'make_plots', 0 ...
% );

% Display results
fprintf('MATLAB latenzy output:\n');
fprintf('Latency: %.6f\n', latency);
fprintf('p-values: ');
disp(s_latenzy.pValsPeak);