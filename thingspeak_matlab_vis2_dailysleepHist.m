%% Thingspeak Matlab Visualisation 2
%% Reading One Week of Sleep quality data into MATLAB
 % We begin by specifying a start date and an end date using a |datetime|
 % object. Because we are sending data to ThingSpeak once every 15 seconds,
 % we have approximately 40,000 data points to retrieve.  ThingSpeak allows
 % only 8000 points in a single read operation, so we create a  |for loop|
 % to gather the data in batches.  We then append the traffic and time data
 % from each iteration into two vectors, called |allsleepData| and
 % |timestamp|.
endDate = datetime('27/9/2016', 'InputFormat', 'dd/MM/yyyy');
startDate = datetime('20/9/2016', 'InputFormat', 'dd/MM/yyyy');
% Create date vector
dateVector = startDate: endDate;
% check to see that the last dateVector value is the same as endDate, if
% not append it 
if (dateVector(end) ~= endDate)
   dateVector = [dateVector, endDate]; 
end
allsleepData = [];
timestamp = [];
% Read data in chunks because ThingSpeak has a limit of 8000 pts per read
for dayCount = 1:length(dateVector)-1
   dateRange = [dateVector(dayCount), dateVector(dayCount+1)];
   [channelData, t] = thingSpeakRead(68285,'Fields',[1,2,3], 'DateRange', dateRange);
   [allsleepData] = [allsleepData; channelData ];
   [timestamp] = [timestamp; t];
end

%% Daily Sums of Sleep Quality as a histogram
% To visualize the volume of sleep ever day, we must sum sleep data and 
% use a bar chart to visualize it. 
sleepTrend = allsleepData(:,1);
sleepDuration = allsleepData(:,2);
sleepQuality = allsleepData(:,3);
for i=1:4  % remove a few pts to be evenly divisible by 5647 (points in a day)
sleepTrend(i) = [];
sleepDuration(i) = [];
sleepQuality(i) = [];
end
% Divide data into 7 parts for each day
dailysum = sum(sleepQuality, floor(length(allsleepData)/7));
dates = dateVector; % convert to serial date for bar plot
dates(8) = [];
dates = datenum(dates);
figure
bar(dates,dailysum)
grid on
xlabel('Date')
ylabel('Sleep Quality')
ax = gca;
ax.YAxis.Exponent = 3;
title('Sleep Quality in the week')
datetick