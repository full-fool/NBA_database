select (count(distinct(swipe.user_id))) / (select count(*) from sat_flashcard_signups  sfg1 where sfg1.created_at >= '2015.4.27' AND sfg1.created_at <='2015.5.4' )  AS retention_rate
from sat_flashcard_swipe swipe,  sat_flashcard_signups signups, thirdTable
where swipe.created_at - '2015-5-4' >= (thirdTable.delta_week) * 7 
	AND swipe.created_at - '2015-5-4' < ((thirdTable.delta_week + 1) * 7)
	AND swipe.user_id = signups.user_id
group by thirdTable.delta_week
