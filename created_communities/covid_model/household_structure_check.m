% Checking the household structure

clear;
load('hs_and_age')
% Total number of households without RH and hospitals
ntot = 28073;

% Accidental in the retirement homes
ind=find(data(1,2:end)<60)
ind=find(data(2,2:end)<60)
ind=find(data(3,2:end)<60)
ind=find(data(4,2:end)<60)
ind=find(data(5,2:end)<60)

% At least one adult in each household
for i=7:size(data,1)
    temp = data(i,~isnan(data(i,:)));
    ind = find(temp(2:end)>=18);
    if (isempty(ind))
        disp(ind)
        disp(i)
    end
end

% Number of families
% Compare against (1-fr.couples no children)*fr_families
num_fam = 0;
fr_cno_ch = 0.49;
fr_f = 0.6727;
for i=7:size(data,1)
    temp = data(i,~isnan(data(i,:)));
    ind = find(temp(2:end)<18);
    if (~isempty(ind))
        num_fam = num_fam + 1;
    end
end
disp('Expected families with children')
disp((1-fr_cno_ch)*fr_f)
disp('Actual')
disp(num_fam/ntot)

% Fraction of single parent families
num_sp = 0;
ac_sp = 0.25;
for i=7:size(data,1)
    temp = data(i,~isnan(data(i,:)));
    ind = find(temp(2:end)<18);
    indp = find(temp(2:end)>=18 & temp(2:end)<=60);
    if (~isempty(ind) & size(indp,2) == 1)
        num_sp = num_sp + 1;
    end
end
disp('Expected single parent families')
disp(ac_sp)
disp('Actual')
disp(num_sp/(fr_f*ntot))

% Households with a person 60+
num_hs60 = 0;
ac_60hs = 0.423;
for i=7:size(data,1)
    temp = data(i,~isnan(data(i,:)));
    indp = find(temp(2:end)>=60);
    if (~isempty(indp))
        num_hs60 = num_hs60 + 1;
    end
end
disp('Expected % households with a person 60+')
disp(ac_60hs)
disp('Actual')
disp(num_hs60/ntot)

% Plot household age distribution
% clrB = [23/255, 119/255, 215/255];
% for i=7:500:size(data,1)
%     temp = data(i,~isnan(data(i,:)));
%     scatter(temp(1)*ones(size(temp,2)-1,1),temp(2:end), 46, clrB, 'filled')
%     hold on
%     clrB = [rand(1), rand(1), 215/255];
% end

%% Work statistics

load('hs_and_work')

% Check if no agent in the retirement home or hospital patient works
for i=1:6
    for j=2:length(data_work(i,:))
        if strcmp(data_work(i,j), 'True')
            disp('Agent in an RH or hospital patient is employed')
            disp(i)
            disp(j)
        end
    end
end

% Compute fraction of households with at least one working agent
n_working_hs = 0;
for i=7:size(data_work,1)
    wflag = 0;
    for j=2:length(data_work(i,:))
        if strcmp(data_work(i,j), 'True')
            wflag = 1;
        end
    end
    if wflag
       n_working_hs = n_working_hs + 1;
       wflag = 0;
    end
end
disp('Households with at least one working agent')
n_working_hs/ntot

% % Collect number of agents working in each household
% for i=7:size(data_work,1)
%     n_work_hs(i-6) = 0;
%     for j=2:length(data_work(i,:))
%         if strcmp(data_work(i,j), 'True')
%             n_work_hs(i-6) = n_work_hs(i-6) + 1; 
%         end
%     end
% end
% 
% % Then find and plot occurences of each number
% n_uq = unique(n_work_hs);
% prct_uq = zeros(size(n_uq));
% for i=1:length(n_uq)
%     ind = find(n_work_hs == n_uq(i));
%     prct_uq(i) = length(ind)/length(n_work_hs)*100;
% end
% pie(prct_uq)

% Collect number of agents working in each family
% n_work_hs = zeros(size(data_work_fam,1),1);
% for i=1:size(data_work_fam,1)
%     n_work_hs(i) = 0;
%     for j=2:length(data_work_fam(i,:))
%         if strcmp(data_work_fam(i,j), 'True')
%             n_work_hs(i) = n_work_hs(i) + 1; 
%         end
%     end
% end
% 
% % Then find and plot occurences of each number
% n_uq = unique(n_work_hs);
% prct_uq = zeros(size(n_uq));
% for i=1:length(n_uq)
%     ind = find(n_work_hs == n_uq(i));
%     prct_uq(i) = length(ind)/length(n_work_hs)*100;
% end
% prct_adjusted = [prct_uq(1), prct_uq(2), sum(prct_uq(3:end))]
% pie(prct_adjusted)

% %% Workplace IDs
% load('house_work_IDs')
% % Number of households where all members work at the same place
% % -1 is hospital, 0 is no workID
% n_same_work = 0;
% for i=1:size(hswIDs,1)
%     temp = hswIDs(i,~isnan(hswIDs(i,:)));
%     non_zero = size(find(temp(2:end)>0 | temp(2:end)==-1),1);
%     n_uq = unique(temp(2:end));
%     if non_zero == (n_uq - 1)
%         n_same_work = n_same_work + 1;
%     end
% end
% disp('Fraction working at the same workplace')
% n_same_work/size(hswIDs,1)
% 
% %% School attendance 
% load('hs_school')
% 
% % First check if no retirement home or hospital patients are attending
% for i=1:6
%     for j=2:length(schools(i,:))
%         if strcmp(schools(i,j), 'True')
%             disp('Agent in an RH or hospital patient attends school')
%             disp(i)
%             disp(j)
%         end
%     end
% end







