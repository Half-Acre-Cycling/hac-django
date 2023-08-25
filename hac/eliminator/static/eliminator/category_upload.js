document.addEventListener("DOMContentLoaded", () => {
    const droppable = document.querySelector('.file-dropzone');
    const originalText = droppable.querySelector('div').innerHTML;
    const input = droppable.querySelector('input');
    const fileChanged = () => {
        var files = input.files;
        if (files.length) {
            droppable.querySelector('span').style.display = 'block';
            droppable.querySelector('div').innerHTML = '';
            const displayTextArray = [];
            for (const file of files) {
                displayTextArray.push(file.name);
            }
            const displayText = `${displayTextArray.join(', ')} - Ready for Upload`;
            droppable.querySelector('div').innerHTML = displayText;
            droppable.classList.add('ready');
        } else {
            droppable.querySelector('div').innerHTML = originalText;
            droppable.classList.remove('ready');
            droppable.querySelector('span').style.display = 'none';
        }
    };
    input.addEventListener('change', fileChanged);
    fileChanged(input);
    droppable.querySelector('span').addEventListener('click', () => {
        input.value = '';
        fileChanged(input);
    });
});