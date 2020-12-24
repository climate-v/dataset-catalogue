

function outputFuse(fuse, iid, oid, arr) {
    document.getElementById(iid).addEventListener("input", function(e) {
        let result = fuse.search(this.value);
        document.getElementById(oid).innerHTML = "";
        result.forEach(function(item) {
            var namelist = "<li>" + arr[item.refIndex] + "</li>";
            document.getElementById(oid).innerHTML += namelist;
        });
    });
}

import Fuse from 'https://cdn.jsdelivr.net/npm/fuse.js@6.4.3/dist/fuse.esm.js'
const options = {
    includeScore: true,
    minMatchCharLength: 2,
    threshold: .4
};

const fuse_countries = new Fuse(countries, options);
outputFuse(fuse_countries, "search", "searchresults", countries)

const fuse_regions = new Fuse(regions, options);
outputFuse(fuse_regions, "regions", "detailedsearchresults", regions)
