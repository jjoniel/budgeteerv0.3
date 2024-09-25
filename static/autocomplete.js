function autocomplete(inp, arr) {
    /*the autocomplete function takes two arguments,
    the text field element and an array of possible autocompleted values:*/
    var currentFocus;
    
    inp.addEventListener("input", function(e) {
        var val = this.value.trim();
        
        // close other autocomplete lists
        closeAllLists();
        if (!val || val.length < 2) 
            return false;
        currentFocus = 0;

        value = val.toUpperCase()
        updated = ""
        for(let e of value) {
            if(e === '&') {
                updated += "AND"
            }
            else if(e === "," || e === "'" || e == ".") {
                continue
            }
            else {
                updated += e
            }
        }
        value = updated

        let found = false
        for (i = 0; i < arr.length; i++) {
            if (arr[i].includes(value)) 
            {
                found = true
                break;
            }
        }
        if(!found)
            return false;

        var a, b, i;
        
        // creates div to hold the values
        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");

        // append the div to parent
        this.parentNode.appendChild(a);

        for (i = 0; i < arr.length; i++) {
            if (arr[i].substr(0, value.length).toUpperCase() == value.toUpperCase()) {
                b = document.createElement("DIV");
                b.innerHTML = "<strong>" + arr[i].substr(0, value.length) + "</strong>";
                b.innerHTML += arr[i].substr(value.length);
                b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
                b.addEventListener("click", function(e) {
                    inp.value = this.getElementsByTagName("input")[0].value;
                    inp.dispatchEvent(new Event("input"));
                    closeAllLists();
                });
                a.appendChild(b);
            }
            else if (arr[i].includes(value)) {
                b = document.createElement("DIV");
                b.innerHTML = arr[i].substr(0, arr[i].indexOf(value));
                b.innerHTML += "<strong>" + arr[i].slice(arr[i].indexOf(value), arr[i].indexOf(value)+value.length) + "</strong>";
                b.innerHTML += arr[i].substr(arr[i].indexOf(value)+value.length);
                b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
                b.addEventListener("click", function(e) {
                    inp.value = this.getElementsByTagName("input")[0].value;
                    inp.dispatchEvent(new Event("input"));
                    closeAllLists();
                });
                a.appendChild(b);
            }
        }
        setTimeout(function() {
            var x = document.getElementById(inp.id + "autocomplete-list");
            console.log(x)
            if (x) {
                addActive(x.getElementsByTagName("div"));
            }
        }, 50);
    });

    inp.addEventListener("keydown", function(e) {
        var x = document.getElementById(this.id + "autocomplete-list");
        if (x) 
            x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
          currentFocus++;
          addActive(x);
        } else if (e.keyCode == 38) { 
          currentFocus--;
          addActive(x);
        } else if (e.keyCode == 13) {
          e.preventDefault();
          if (currentFocus > -1) {
            if (x) 
                x[currentFocus].click();
          }
        }
    });

    function addActive(x) {
        if (!x) return false;
        removeActive(x);
        if (currentFocus >= x.length) 
            currentFocus = 0;
        if (currentFocus < 0) 
            currentFocus = (x.length - 1);
        x[currentFocus].classList.add("autocomplete-active");
    }

    function removeActive(x) {
      for (var i = 0; i < x.length; i++) {
        x[i].classList.remove("autocomplete-active");
      }
    }

    // closes the all unselected autocomplete lists
    function closeAllLists(elmnt) {
        var x = document.getElementsByClassName("autocomplete-items");
        if (x) {
            for (var i = 0; i < x.length; i++) {
                if (elmnt != x[i] && elmnt != inp) {
                    x[i].parentNode.removeChild(x[i]);
                }
            }
        }
    }

  document.addEventListener("click", function (e) {
      closeAllLists(e.target);
  });
}