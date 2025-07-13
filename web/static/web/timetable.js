function cell_changed(input) {
    if (input.value == '-') {
        input.parentNode.className = 'cell-available';
    } else if (input.value != '') {
        input.parentNode.className = 'cell-lesson';
    } else {
        input.parentNode.className = '';
    }
}

function save(input) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const col = input.getAttribute('data-col');
    const hourCell = input.parentNode.parentNode.childNodes[1];
    const value = input.value;
    const body = new FormData();

    body.append('value', value);
    body.append('day_index', col);
    body.append('hour', Number(hourCell.innerText.split(':')[0]));
    body.append('csrfmiddlewaretoken', csrfToken);

    fetch('/update-timetable', {
        body: body,
        method: 'POST'
    }).then((r) => {
        let resultLabel = document.querySelector('.result-label');
        resultLabel.className = '';
        void resultLabel.offsetWidth;
        
        if (r.status == 200) {
            resultLabel.className = 'result-label success';
            resultLabel.innerText = 'Сохранено';
            console.log('Success');
        }
        else {
            resultLabel.className = 'result-label error';
            resultLabel.innerText = 'Не удалось сохранить';
            console.log('Error');
        }
    })
}
