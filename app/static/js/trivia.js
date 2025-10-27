(function(){
    const tiempoTotal = parseFloat("{{ tiempo_total | default(15) }}") || 15;
    let tiempoRestante = tiempoTotal;
    const fill = document.getElementById('timer-fill');
    const timerText = document.getElementById('timer-seconds');
    const optionButtons = Array.from(document.querySelectorAll('.opt-btn'));
    const opcionInput = document.getElementById('opcion_id');
    const tiempoInput = document.getElementById('tiempo_restante');
    const form = document.getElementById('answerForm');
    const tickMs = 100;
    let intervalId = null;
    let answered = false;
        //empieza el timer al cargar la pagina
    function startTimer(){
        tiempoRestante = tiempoTotal;
        updateTimerUI();
        intervalId = setInterval(() => {
            tiempoRestante = Math.max(0, tiempoRestante - tickMs/1000);
            updateTimerUI();
            if (tiempoRestante <= 0){
                clearInterval(intervalId);
                timeoutSubmit();
            }
        }, tickMs);
    }

    function updateTimerUI(){
        fill.style.width = (tiempoRestante / tiempoTotal * 100) + '%';
        timerText.textContent = Math.ceil(tiempoRestante) + 's';
    }
    /* desactiva el cliqueo después de contestar */
    function disableOptions(){
        optionButtons.forEach(b => b.disabled = true);
    }
    /* muestra las opciones correctas e incorrectas con colores*/
    function showCorrectIncorrect(btn){
        const correcta = btn.dataset.correcta === "True";
        disableOptions();

        if (correcta){
            btn.style.backgroundColor = '#28a745'; // verde
        } else {
            btn.style.backgroundColor = '#dc3545'; // rojo
            // marcar la correcta en verde
            const correctaBtn = optionButtons.find(b => b.dataset.correcta === "True");
            if (correctaBtn) correctaBtn.style.backgroundColor = '#28a745';
        }
    }
    /* recibe la opcion contestada y guarda el tiempo para calcular score*/
    function submitAnswer(opid){
        answered = true;
        clearInterval(intervalId);
        opcionInput.value = opid;
        tiempoInput.value = Math.ceil(tiempoRestante);
            /* pasa a la siguiente pregunta*/
        setTimeout(() => {
            const fd = new FormData(form);
            fetch(form.action, {
                method: 'POST',
                body: fd,
                credentials: 'same-origin'
            }).then(_ => {
                window.location.href = "/trivia/partida";
            }).catch(err => {
                console.error(err);
                form.submit();
            });
        }, 1000);
    }
    
    function timeoutSubmit(){
        if (answered) return;
        answered = true;
        disableOptions();
        opcionInput.value = 0;
        tiempoInput.value = 0;

        // muestra la correcta
        const correctaBtn = optionButtons.find(b => b.dataset.correcta === "True");
        if (correctaBtn) correctaBtn.style.backgroundColor = '#28a745';

        setTimeout(() => {
            const fd = new FormData(form);
            fetch(form.action, {
                method: 'POST',
                body: fd,
                credentials: 'same-origin'
            }).then(_ => window.location.href = "/trivia/partida")
              .catch(err => form.submit());
        }, 1000);
    }

    optionButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            if (answered) return;
            showCorrectIncorrect(btn);
            submitAnswer(btn.dataset.opid);
        });
    });

    window.addEventListener('load', startTimer);

})();