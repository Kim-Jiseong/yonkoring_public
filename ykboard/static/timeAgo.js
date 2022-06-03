function TimeAgo(post_time, timeDom){
    timeDom.style.display = 'block'
    // 현재시간
    const today = new Date();
    const now = today.toLocaleString();
    const year = now.split('.')[0]
    const date = now.split('.')[1].trim() + '/' + now.split('.')[2].trim()
    const morning_afternoon = now.split(' ')[3]
    const time = now.split(' ')[4].split(':')[0]+':'+now.split(' ')[4].split(':')[1]
   
    // 포스트 시간
    const postDay = post_time
    const postYear = postDay.split("년")[0]
    const postDate = postDay.split("년")[1].split("월")[0].trim() + '/' + postDay.split("년")[1].split("월")[1].split("일")[0].trim()
    const post_morning_afternoon = postDay.split(' ')[4]
    const postTime= postDay.split(' ')[3]


    // 날짜가 같을 때
    if(year === postYear && date === postDate){
        // 시간이 같을 때
        if(morning_afternoon === post_morning_afternoon && time === postTime){
            timeDom.innerHTML = '방금 전'
        }
        // 시간이 다를 때
        else{
            // 1시간 이내일 때
            if(morning_afternoon === post_morning_afternoon && time.split(':')[0] == postTime.split(':')[0] ){
                const ago = time.split(':').join('') - postTime.split(':').join('')
                timeDom.innerHTML = `${ago}분 전`
            }
            else{
                timeDom.innerHTML = `${post_morning_afternoon} ${postTime}`
            }
        }
    }
    // 날짜가 다를 때
    else{
        // 년도가 같을 때
        if(year === postYear){
            timeDom.innerHTML = `${postDate} ${post_morning_afternoon} ${postTime}`
        }
        else{
            timeDom.innerHTML = `${postYear}/${postDate} ${post_morning_afternoon} ${postTime}`
        }
    }

}