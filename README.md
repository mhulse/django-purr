# Django Purr

```
......................................
........../\............./\...........
........./..\.........../..\..........
.......././\.\__-----__/./\.\.........
......./.....................\........
......|.....(.o.).__.(.o.)....|.......
.....~~~~~~...../.ºº.\.....~~~~~~.....
...~~~~~~....(.../--\...)....~~~~~~...
........\\.......PURR.......//........
............\\\/\/||\/\///............
..................\/..................
......................................
```

### Testing a solution to read unlimited categories from a URI.

---

#### ABOUT

The `Category` model was taken from [Satchmo Project](http://www.satchmoproject.com/), I've only added slight modifications.

**Note:** Tested using Django `(1, 3, 0, 'final', 0)`.

---

#### DISCUSSION

[Django categories, sub-categories and sub-sub-categories](http://stackoverflow.com/a/9492349/922323)

---

#### INSTALLATION

Using [PIP](http://www.pip-installer.org).

The repository will be checked out in a temporary folder, installed, and cleaned up:

```bash
$ pip install git+https://github.com/mhulse/django-purr.git
```

This can be combined with the `-e` flag, and Pip will perform the checkout in `./src/`. You need to supply a name for the checkout folder by appending a hash to the repository URL:

```bash
$ pip install -e git+https://github.com/mhulse/django-purr.git#egg=django-purr
```

More info [here](http://www.pip-installer.org/en/latest/usage.html#version-control-systems).

Next, add `purr` to your `INSTALLED_APP` in your app's `settings.py`:

```python
INSTALLED_APPS = (
    # ...
    'purr',
    # ...
)
```

Finally, add this to your app's `urls.py` tuple:

```python
urlpatterns = patterns('',
    # ...
    (r'^purr/', include('purr.urls')),
    # ...
)
```

---

#### EXAMPLES

Given this URI:

```html
http://site.com/purr/business/delivery-only/italian/pizza/
```

… the output will be:

```json
{
    "category": "Pizza"
}
```

The code itterates over each sequential category `slug` and and will throw a `Page not found (404)` if the category structure doesn't exist; for example:

```html
http://testprojects.registerguard.com/djcat/business/delivery-only/ddd/pizza/
```

There's a tester script, found in the `scripts` folder, that you can run like so:

```bash
$ python manage.py runscript purr_tests
```

… the output will be (it will help if you've installed the `initial_data.json` fixture):

```bash
[<Category: Business>,
 <Category: BUSINESS | Sports>,
 <Category: BUSINESS | SPORTS | Eating contest>,
 <Category: BUSINESS | SPORTS | EATING CONTEST | Pizza>]
```

---

#### LEGAL

Copyright © 2012 [Micky Hulse](http://hulse.me)

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this work except in compliance with the License. You may obtain a copy of the License in the LICENSE file, or at:

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.