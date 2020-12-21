import Fuse from 'https://cdn.jsdelivr.net/npm/fuse.js@6.4.3/dist/fuse.esm.js'
const options = {
    includeScore: true,
    minMatchCharLength: 2,
    threshold: .4
};
const fuse = new Fuse(countries, options);

document.getElementById("search").addEventListener("input", function(e) {
    let result = fuse.search(this.value);
    document.getElementById("searchresults").innerHTML = "";
    result.forEach(function(item) {
        var namelist = "<li>" + countries[item.refIndex] + "</li>";
        document.getElementById("searchresults").innerHTML += namelist;
    });
});
