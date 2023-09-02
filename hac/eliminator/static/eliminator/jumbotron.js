let currentCategory = 0;
const cycleResults = () => {
    console.log(`current category: ${currentCategory}`)
    const categories = document.querySelectorAll('.results_category');
    for (let i = 0; i < categories.length; i++) {
        const category = categories[i];

        category.classList.remove('hidden');
        if (i != currentCategory) {
            category.classList.add('hidden');
        } else {
            const title = category.getAttribute('category');
            document.querySelector('#results-identifier').innerHTML = `${title} Results`
        }
    }
    
    currentCategory++;
    if (currentCategory === categories.length) currentCategory = 0;
    
}

document.addEventListener('DOMContentLoaded', () => {
    // reload page once every 3 minutes
    setTimeout(() => {
        window.location.reload();
    }, 180000);
    cycleResults();
    setInterval(cycleResults, 20000);
})