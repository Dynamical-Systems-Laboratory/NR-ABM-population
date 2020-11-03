clear
data = load('test_data/agents_out.txt');

%% Plot unique households and number of agents in each
% all_houses = unique(data(:,6));
% all_houses = all_houses(all_houses~=0);
% 
% households = zeros(length(all_houses),1);
% for i=1:length(all_houses)
%     households(i) = length(find(data(:,6)==all_houses(i)));
% end
% figure(1), plot(sort(households),'o-')

%% Check age structure in the households
% for i=1:length(all_houses)
%     ind = find(data(:,6)==all_houses(i));
%     disp(data(ind,3))
%     pause
% end

%% Check school types and ages
% ind = find(data(:,1)==1);
% plot(sort(data(ind,3)),'v')
% % Check if no agent in a school elementary - high is omitted
% % Should be empty
% ind = find(data(:,3)>=5 & data(:,3)<=17 & data(:,1)==0 & data(:,7)==0);
% disp(length(ind))
% % Schools sizes
% all_schools = unique(data(:,8));
% all_schools = all_schools(all_schools~=0);
% schools = zeros(length(all_schools),1);
% for i=1:length(all_schools)
%     schools(i) = length(find(data(:,8)==all_schools(i)));
% end
% figure(2), plot(sort(schools),'v-')

%% Check hospitals
% ind = find(data(:,10)==1);
% for i=1:length(ind)
%     disp(data(ind(i),:))
% end

%% Check all other workplaces
% Check if all working agents within working age
ind = find(data(:,2)==1);
plot(sort(data(ind,3)),'s-')
% Check if correct unemployement 
n_emp = length(ind)

% Check if all workplaces have correct number of employees
all_works = unique(data(:,9));
all_works = all_works(all_works~=0);
works = zeros(length(all_works),1);
for i=1:length(all_works)
    works(i) = length(find(data(:,9)==all_works(i)));
end
figure(1), plot(sort(works),'o-')
works
% All agents that work need to have house ID
length(find(data(:,2)==1 & data(:,6)~=0))
% And cannot be in a retirement home
sort(data(find(data(:,2)==1 & data(:,6)~=0),6))



