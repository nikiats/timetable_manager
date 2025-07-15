function cell_changed(input) {
    if (input.value == '-') {
        input.parentNode.className = 'cell-available';
    } else if (input.value != '') {
        input.parentNode.className = 'cell-lesson';
    } else {
        input.parentNode.className = '';
    }
}

function cell_keydown(input, event) {
    if (event.key == 'Enter') {
        input.blur();
    }
}

function cell_focus(input) {
	input.setAttribute("prevValue", String(input.value));
}

function cell_save(input) {
	console.log(input.prevValue, input.value);
	if (input.getAttribute("prevValue") == input.value) {
		return;
	}

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const col = input.getAttribute('data-col');
    const hourCell = input.parentNode.parentNode.childNodes[1];
    const value = input.value;
    const body = new FormData();

    body.append('value', value);
    body.append('day_index', col);
    body.append('hour', Number(hourCell.innerText.split(':')[0]));
    body.append('csrfmiddlewaretoken', csrfToken);

	let resultLabel = document.querySelector('.result-label');
	resultLabel.className = '';
	void resultLabel.offsetWidth;

    fetch('/update-timetable', {
        body: body,
        method: 'POST'
    }).then((r) => {
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
    }).catch((r) => {
		resultLabel.className = 'result-label error';
		resultLabel.innerText = 'Не удалось сохранить';
		console.log('Error (catch)');
	})
}
