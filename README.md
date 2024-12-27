# (LLM) Image Describer

Personal experiments in Python to generate text description of my entire old Soup.io archive (~32k images), so that the images have alt text and can be searched using lunr.js.

## Usage: generate descriptions

Generate text descriptions saved alongside image files (e.g. file `images/funny/001.jpg` will have its description in `images/funny/001.txt`).

`python describe_ollama.py path_to_images`

`python describe_claude_haiku.py path_to_images`

## Usage: generate JSON for lunr.js

`python search.py path_to_images`

The resulting `assets_index` json will contain all image paths and their text descriptions.

## Usage: client-side full-text search with lunr.js

```
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Search</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/lunr.js/2.3.9/lunr.min.js"></script>
</head>
<body>
  <h1>Search</h1>
  <input type="text" id="searchBox" placeholder="Search...">
  <ul id="results"></ul>

  <script>
    let idx;
    let data;

    // Load the data from assets_index.json
    fetch('./assets_index.json')
      .then(response => response.json())
      .then(json => {
        data = json;
        idx = lunr(function () {
          this.ref('asset_path');
          this.field('description');

          data.forEach(function (doc) {
            this.add(doc);
          }, this);
        });
      });

    document.getElementById('searchBox').addEventListener('input', function () {
      const query = this.value;
      const results = idx.search(query);
      const resultsList = document.getElementById('results');
      resultsList.innerHTML = '';

      results.forEach(result => {
        const item = data.find(d => d.asset_path === result.ref);
        console.log(item);
        const li = document.createElement('li');
        li.textContent = item.description;
        li.textContent += ' - ' + item.asset_path;
        resultsList.appendChild(li);

        const li2 = document.createElement('li');
        const img = document.createElement('img');
        img.src = "https://somebasepath" + item.asset_path;
        li2.appendChild(img);
        resultsList.appendChild(li2);
      });
    });
  </script>
</body>
</html>
```

