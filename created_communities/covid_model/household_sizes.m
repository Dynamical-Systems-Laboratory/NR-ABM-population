%% Plot household and building sizes

clear

% Residential building sizes
% hs = load('check_bld_size_w_coords.txt');
% 
% ind = find(hs(:,2)<3);
% scatter(hs(ind,3), hs(ind,4), 16, [59/255, 166/255, 26/255], 'filled' )
% hold on
% 
% ind = find(hs(:,2)>=3 & hs(:,2)<10);
% scatter(hs(ind,3), hs(ind,4), 16, [129/255, 222/255, 36/255], 'filled')
% 
% ind = find(hs(:,2)>=10 & hs(:,2)<100);
% scatter(hs(ind,3), hs(ind,4), 16, [243/255, 221/255, 18/255],'filled')
% hold on
% 
% ind = find(hs(:,2)>=100 & hs(:,2)<500);
% scatter(hs(ind,3), hs(ind,4), 16, [255/255, 153/255, 0/255], 'filled')
% 
% ind = find(hs(:,2)>=500);
% scatter(hs(ind,3), hs(ind,4), 16, [203/255, 45/255, 6/255],'filled')
% 
% legend('<3', '3-10', '10-100', '100-500', '500+', 'FontSize', 12)
% daspect([1 1 1])

% Household size - pie chart
hs = load('check_household_size.txt');
h_sizes = unique(hs(7:end, 2));
hs = hs(7:end, :);

prct_uq = zeros(size(h_sizes));
for i=1:length(h_sizes)
    ind = find(hs(:,2) == h_sizes(i));
    prct_uq(i) = length(ind)/length(hs(:,1))*100;
end
prct_adjusted = [prct_uq(1), prct_uq(2), prct_uq(3), sum(prct_uq(4:end))]
pie(prct_adjusted)
