%% Thingspeak Matlab Visualisation 1
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
%% Plotting Raw Sleep Data
% Next we plot the data and label the graph. The daily fluctuations in
% sleep are clearly visible from the raw data.
figure
plot(timestamp, allsleepData)
datetick
xlabel('Date')
ylabel('Sleep Trend')
grid on
title('Daily Sleep trend')
legend('Sleep trend','Sleep duration','Sleep quality')