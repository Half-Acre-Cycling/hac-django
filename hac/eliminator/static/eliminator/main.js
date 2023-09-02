/**
 * Handle Expanding rider details
 */
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('.rider').forEach((el) => {
        const header = el.querySelector('.header');
        header.addEventListener('click', () => {
            if (el.classList.contains('expanded')) {
                el.classList.replace('expanded', 'unexpanded');
            } else el.classList.replace('unexpanded', 'expanded');
        });
    });
});

const storeCurrentPlacingInSessionStorage = () => {
    const dataObj = {};
    document.querySelectorAll('.sort-zone').forEach((zone) => {
        const key = zone.id;
        const values = [];
        zone.querySelectorAll('.rider').forEach((rider) => {
            const id = rider.id.split('_')[1];
            values.push(id);
        });
        dataObj[key] = values;
    });
    window.sessionStorage.setItem('placing', JSON.stringify(dataObj));
}

const addPlaces = (zone) => {
    // assign scoring based on (new) sorting
    const placingRiders = zone.querySelectorAll('.rider');
    for (let i = 0; i < placingRiders.length; i++) {
        const place = i + 1;
        const header = placingRiders[i].childNodes[1];
        header.setAttribute('place', place.toString());
    }
}

/**
 * Sorting and drag/drop
 */
const sortableList = (e) => {
    e.preventDefault();
    let sortZoneId;
    if (e.target.classList.contains('sort-zone')) {
        // target is sort zone
        sortZoneId = e.target.id;
    } else {
        // target parentElement is _probably_ the sort zone
        sortZoneId = e.target.parentElement.id;
        // but it could also be the parent of the parent, depending on the dragover target
        if (sortZoneId.indexOf('rider') !== -1) sortZoneId = e.target.parentElement.parentElement.id;
    }
    try {
        const zone = document.querySelector(`#${sortZoneId}`);
        const draggedRider = document.querySelector('.rider.dragging');
        const siblingRiders = [...zone.querySelectorAll('.rider:not(.dragging)')];
        const nextSiblingRider = siblingRiders.find((rider) => {
            return e.clientY <= rider.offsetTop + rider.offsetHeight / 2;
        });
        zone.insertBefore(draggedRider, nextSiblingRider);
        if (sortZoneId === 'placing_results') {
            addPlaces(zone);
        } else {
            draggedRider.childNodes[1].setAttribute('place', '');
        }
        storeCurrentPlacingInSessionStorage();
    } catch (er) {
        console.log(er);
    }
}
document.addEventListener('DOMContentLoaded', () => {
    // sortable/dragging functions
    document.querySelectorAll('.sort-zone').forEach((zone) => {
        if (zone.id === 'placing_results') {
            addPlaces(zone);
        }
        zone.addEventListener('dragover', sortableList);
        zone.addEventListener('dragenter', e => e.preventDefault());
        zone.querySelectorAll('.rider').forEach((rider) => {
            rider.addEventListener('dragstart', () => {
                setTimeout(() => {
                    rider.classList.add('dragging');
                }, 0);
            });
            rider.addEventListener('dragend', () => rider.classList.remove('dragging'));
        });
    });
    // update results button click
    const scoringButtonEl = document.querySelector('#update_placing');
    if (scoringButtonEl) {
        scoringButtonEl.addEventListener('click', ()=> {
            const csrf = document.querySelector('input[name=csrfmiddlewaretoken]').value;
            const placing = window.sessionStorage.getItem('placing');
            if (placing) {
                window.sessionStorage.removeItem('placing');
                fetch(window.location.href, {
                    method: 'post',
                    body: placing,
                    headers: {
                        'X-CSRFToken': csrf
                    }
                }).then(response => window.location.reload());
            }
        });
    }
    // add placing on initial page load

});