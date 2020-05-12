%% Thingspeak Matlab analysis for daily sleep data
% For each day, we specify a start time and a stop time.
clear all
startTime{1} = 'September 20, 2016 00:00:00';
stopTime{1} = 'September 20, 2016 23:59:59';
% We retrieve the data from ThingSpeak, and we
% downsample the data to remove short-term fluctuations.  We then use the
% findpeaks function to plot and find the times where sleep trend fluctuation
% is highest. For ease of use we only use sleep trend data.
startDate = datetime(startTime{1}, 'InputFormat', 'MMMM d, yyyy HH:mm:ss ');
endDate = datetime(stopTime{1}, 'InputFormat', 'MMMM d, yyyy HH:mm:ss ');
datevector = [startDate, endDate];
[Daily, t] = thingSpeakRead(68285,'Fields',[1], 'DateRange', datevector);
Dailysleep = Daily(:, 1);
timestamp = datetime(t,'ConvertFrom','datenum'); 
dateAnalyzed = startTime{1};
dateAnalyzed = {dateAnalyzed(1:(end-8))};
%% Downsampling into 48 Bins of 30 Minute Chunks of Data and Finding Peaks
% The raw sleep data is very fluctuating and hard to visualize.  If we want to
% see what time of day has the highest volume of sleep trend, we need to look
% at the data on a time scale larger than 15 seconds. To do this we divide
% the 24 hour day into 30 minute segments.  Each segment begins at the top
% of the hour and ends 30 minutes later.
downsamplesize = floor(length(Dailysleep)/48);
tsleepper30=datetime(startTime{1});
Dailysleepper30(1:48) = 0; % pre-allocate
for k = 1:48  % calucate daily tarffic in each 30 minute segment
Dailysleepper30(k) = sum(Dailysleep(1+downsamplesize*(k-1):downsamplesize*k));
tsleepper30(k+1) = tsleepper30(k)+1/48; % timestamps showing end of each 30 minute period
end
tsleepper30=tsleepper30';
tsleepper30(1) = []; % start first bin at 12:30 am
timestampPer30 = tsleepper30;
% Find peaks and their times (locations)
[peaks,location] = findpeaks(Dailysleepper30,  'Threshold',100, 'MinPeakHeight', 1100);
% Plot peaks
figure
findpeaks(Dailysleepper30, datenum(timestampPer30),'Threshold',100, 'MinPeakHeight', 1100)
datetick
xlabel('Time of Day')
ylabel('Sleep Trend for 30 min')
title(strcat('Peak volume on ', {' '}, dateAnalyzed)) 
dateAnalyzed
peaktimes = timestampPer30(location)
DailyVolume = sum(Dailysleep);
analyzedData = [peaktimes; DailyVolume]

 
% So far we have brought the data from ThingSpeak back into MATLAB to do
% some offline analysis of weekly and daily sleep patterns, now we send back
% analysed data into thingspeak channel to visualize anytime

thingSpeakWrite(108284, analyzedData);
