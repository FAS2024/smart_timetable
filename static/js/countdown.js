
const quizStartDate = document.getElementById("quiz-start-date")
const quizEndDate = document.getElementById("quiz-end-date")
const countdownBox = document.getElementById("countdown-box")
const startQuizBtn = document.getElementById("start-quiz")
const endQuizBtn = document.getElementById("can-not-start-quiz")
const allocatedTime = document.getElementById("allocated-time")


const startDate =  Date.parse(quizStartDate.textContent)
const endDate =  Date.parse(quizEndDate.textContent)

const myCountdown = setInterval(()=>{
    const now = new Date().getTime()
    const available = endDate - startDate
    const difference  = startDate - now


    // const day = Math.floor(available / (1000 * 60 * 60 * 24))
    const hour = Math.floor((available / (1000 * 60 * 60)) % 24)
    const minutes = Math.floor((available / (1000 * 60)) % 60)
    const seconds = Math.floor((available / (1000)) % 60)

    const d = Math.floor(startDate / (1000 * 60 * 60 * 24) - (now / (1000 * 60 * 60 * 24)))
    const h = Math.floor((startDate / (1000 * 60 * 60) - (now / (1000 * 60 * 60))) % 24)
    const m = Math.floor((startDate / (1000 * 60) - (now / (1000 * 60))) % 60)
    const s = Math.floor((startDate / (1000) - (now / (1000))) % 60)

    if (difference > 0){
        countdownBox.innerHTML = d + " days, " + h + " hours, " + m + " minutes, " + s + " seconds"
        startQuizBtn.style.display = "none" 
        allocatedTime.innerHTML = "Allocated Time: (" + hour + " H, " + minutes + " m, " + seconds + " s)"

    }else {
        if (available > 0) {
            clearInterval(myCountdown)
            countdownBox.innerHTML = "Quiz in Progress"
            startQuizBtn.style.display = "block" 
            endQuizBtn.style.display = "none"
            
        } else {
            clearInterval(myCountdown)
            startQuizBtn.style.display = "none" 
            endQuizBtn.style.display = "none"
            countdownBox.innerHTML = "(00:00:00)" + " Quiz Completed"
            quizStartDate.style.display = "none"
            quizEndDate.innerHTML = "Quiz has ended"
        }
    }
},1000)

