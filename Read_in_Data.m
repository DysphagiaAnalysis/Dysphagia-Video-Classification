clc;
clear;

% change the directory to the folder which contains the clean_data folders
cd 'C:\Users\song wang\Desktop\UBC\UBC Courses\2021_Winter_Term_1\EECE562 Statistical Signal Processing\Project\EECE562-Project\Eigenvalue_Calc'
% read files in the directory
listing = dir('HB_Anno_E_Clean_Data\');

% change all the following HB_Anno_E_Clean_Data to A, D when necessary

for j=3:length(listing)
    listing(j).name
    T = readtable(fullfile('HB_Anno_E_Clean_Data',listing(j).name));
    T = table2array(T);
    T_x = T(:,3);
    T_y = T(:,4);
    T_x = data_range_adjustment(T_x);
    T_y = data_range_adjustment(T_y);

    [a_x, q_x, sig_x]=HMM_Model(T_x);
    [a_y, q_y, sig_y]=HMM_Model(T_y);
    if not(isfolder('HB_Anno_E_Eigenvalue'))
        mkdir HB_Anno_E_Eigenvalue
    end
    
    % ignore the calculation with Nan Values in a_y and a_x
    if sum(isnan(a_x),'All')==0 && sum(isnan(a_y),'All')==0
        e_x = eig(a_x);
        e_y = eig(a_y);
        display(e_x);
        display(e_y);
        writematrix([vertcat(e_x,sig_x), vertcat(e_y,sig_y)],fullfile('HB_Anno_E_Eigenvalue',append(erase(listing(j).name,'clean_data.csv'),'eigenvalue_noise.csv')));
    end
end

function [y] = data_range_adjustment(y)
    N_normalize = 10;
    max_y = max(y);
    min_y = min(y);
    range_y = max_y - min_y;
    for i = 1:length(y)
        y(i) = (y(i)- min_y)/range_y * 2*N_normalize - N_normalize;
    end    
end

function [a, q, sig] = HMM_Model(y)
% Iteration
N = 1500;

% initialize parameters for estimation
% transition matrix 4 by 4 with constraints
a = [0.5,  0.5,    0,   0;
       0,  0.4,  0.6,   0;
       0,    0,  0.7, 0.3;
       0,    0,    0,   1];
% 4 states for byoid bone movement
q = [1, 2, 3, 4];
% noise variance Gaussian mean 0 
sig = sqrt(1);

for n = 1:N
    [a, q, sig]= EM_HMM(y, a, q, sig);
end

function [a, q, sig] = EM_HMM(y, a, q, sig)
% HMM filter
% Initial pi_k vector for 4 states
pi_k = [0.25, 0.25, 0.25, 0.25]';

% Store all the pi_k B_yK information in matrix for Smoother usage
B_yk_collection = zeros(length(q),length(y)*length(q));
pi_k_collection = zeros(length(q),length(y));

for k = 1:length(y)
    % define the B_yk matrix and update with each new y_k
    B_yk = [normpdf(y(k)-q(1),0, sig),                        0,                         0,                       0;
            0,                         normpdf(y(k)-q(2),0,sig),                         0,                       0;
            0,                                                0,  normpdf(y(k)-q(3),0,sig),                       0;
            0,                                                0,                         0, normpdf(y(k)-q(4),0,sig)
            ];
    % Update pi_k
    pi_k = B_yk * a' *pi_k /(ones(1, length(q))* B_yk * a' *pi_k);
    
    % update pi_k_collection and B_yk_collection for HMM Smoother
    B_yk_collection(:,(4*k-3):(4*k)) = B_yk;
    pi_k_collection(:,k) = pi_k;
end

% HMM Smoother

% initialize beta_k_N = [1,1,1,1]'
beta_k_N = ones(1,length(q))';

% Initialize beta_k_N_collection
beta_k_N_collection = zeros(length(q),length(y));
beta_k_N_collection(:,end) = beta_k_N; 

% initialize pi_k_N_collection
pi_k_N_collection = zeros(length(q),length(y));
pi_k_N_collection(:,end) = pi_k_collection(:,end);

% fix a smoothing widow
% Use observation from 1 to k+fix_interval to smooth x_k
fix_interval = 5;

%count bacwards for HMM Smoother
for l = length(y):-1:1 
    
    if l> length(y) - fix_interval
        % update beta_k_N
        beta_k_N = a * B_yk_collection(:,(4*l-3):(4*l)) * beta_k_N;
        % Normalize beta_k_N
        beta_k_N = beta_k_N/sum(beta_k_N,'All');
        % calculate for pi_k_N
        pi_k_N = pi_k_collection(:,l-1) .* beta_k_N /(pi_k_collection(:,l-1)' * beta_k_N);
        beta_k_N_collection(:,l-1) = beta_k_N;
        pi_k_N_collection(:,l-1) = pi_k_N; 

    else
        % reset beta_k_N
        beta_k_N = ones(1,length(q))';
        % update beta_k_N for the fix_interval times
        for m = fix_interval:-1:1
            % update beta_k_N
            beta_k_N = a * B_yk_collection(:,(4*l+4*m-7):(4*l+4*m-4)) * beta_k_N;
            % Normalize beta_k_N
            beta_k_N = beta_k_N/sum(beta_k_N,'All');
        end
        % update pi_k_N
        if l>1
            pi_k_N = pi_k_collection(:,l-1) .* beta_k_N /(pi_k_collection(:,l-1)' * beta_k_N);
            beta_k_N_collection(:,l-1) = beta_k_N;
            pi_k_N_collection(:,l-1) = pi_k_N;
        end
    end   
end

% EM algorithm to update a, q, sig
% calculate gamma_i, gamma_ij
% gamma_i is the smoother probability

gamma_i = pi_k_N_collection;

% initialize gamma_ij
gamma_ij = zeros(length(q),length(y)*length(q));

 for t = 1:length(y)-1
     gamma_ij(:,(4*t-3):(4*t)) = (a * B_yk_collection(:,(4*t+1):(4*t+4))).*(pi_k_collection(:,t) * beta_k_N_collection(:,t+1)');
     gamma_ij(:,(4*t-3):(4*t)) = gamma_ij(:,(4*t-3):(4*t))/sum(gamma_ij(:,(4*t-3):(4*t)),'All');
 end
 
 % initialize gamma_ij sum and gamma_sum
 gamma_ij_sum = zeros(length(q),length(q));
 gamma_i_sum = zeros(length(q),1);
 gamma_i_yt_sum = zeros(length(q),1);
 gamma_i_yt_qi_square = 0;
 
 for t = 1:length(y)-1
     gamma_ij_sum = gamma_ij_sum + gamma_ij(:,(4*t-3):4*t);
     gamma_i_sum = gamma_i_sum + gamma_i(:,t);
     gamma_i_yt_sum = gamma_i_yt_sum + gamma_i(:,t)*y(t);
     gamma_i_yt_qi_square = gamma_i_yt_qi_square + [(y(t)-q(1))^2, (y(t)-q(2))^2, (y(t)-q(3))^2, (y(t)-q(4))^2] * gamma_i(:,t);
 end
 
  % update a, q, sig based on gamma_i and gamma_ij
  a = [gamma_ij_sum(1,1)/(gamma_ij_sum(1,1)+gamma_ij_sum(1,2)), gamma_ij_sum(1,2)/(gamma_ij_sum(1,1)+gamma_ij_sum(1,2)),                                                       0,                                                       0;
                                                             0, gamma_ij_sum(2,2)/(gamma_ij_sum(2,2)+gamma_ij_sum(2,3)), gamma_ij_sum(2,3)/(gamma_ij_sum(2,2)+gamma_ij_sum(2,3)),                                                       0;
                                                             0,                                                       0, gamma_ij_sum(3,3)/(gamma_ij_sum(3,3)+gamma_ij_sum(3,4)), gamma_ij_sum(3,4)/(gamma_ij_sum(3,3)+gamma_ij_sum(3,4));
                                                             0,                                                       0,                                                       0,                                                       1];
  q = gamma_i_yt_sum ./ gamma_i_sum;
  sig = sqrt(1/(length(y)-1)*gamma_i_yt_qi_square);
  
end
end