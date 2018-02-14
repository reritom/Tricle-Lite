# Tricle-Lite
[ACTIVE] Light, AJAX focused version of Tricle

## Todo

| Task | Description | In Progress | Done |
| :---: | :--- | :---: | :---: |
| `1` | Add downloads remaining and expiration countdown to download div | <ul><li>- [ ] </li></ul> | <ul><li>- [ ] </li></ul> |
| `2` | Refacture views in tools and add certain methods to the model classes (getStatus, etc) | <ul><li>- [ ] </li></ul> | <ul><li>- [x] </li></ul> |
| `3` | https://www.sitepoint.com/build-javascript-countdown-timer-no-dependencies/ | <ul><li>- [ ] </li></ul> | <ul><li>- [ ] </li></ul> |
| `4` | Password for zipfile if phase isnt local | <ul><li>- [x] </li></ul> | <ul><li>- [ ] </li></ul> |
| `5` | Link to GitHub in dropdown | <ul><li>- [ ] </li></ul> | <ul><li>- [ ] </li></ul> |
| `6` | Delete files once processed | <ul><li>- [ ] </li></ul> | <ul><li>- [x] </li></ul> |
| `7` | Create /iaw (cleanup) view | <ul><li>- [ ] </li></ul> | <ul><li>- [ ] </li></ul> |
| `8` | Create /hard (delete and expire everything) view | <ul><li>- [ ] </li></ul> | <ul><li>- [ ] </li></ul> |
| `9` | Create `pre` and `post` dirs to store files in | <ul><li>- [ ] </li></ul> | <ul><li>- [ ] </li></ul> |
| `10` | Add v2 seedgen using hashlib and mixed keys | <ul><li>- [ ] </li></ul> | <ul><li>- [ ] </li></ul> |
| `11` | Move form post to separate endpoint | <ul><li>- [ ] </li></ul> | <ul><li>- [x] </li></ul> |
| `12` | Use the zip token to validate the /down request, make it a POST | <ul><li>- [ ] </li></ul> | <ul><li>- [x] </li></ul> |
| `13` | Encrypt the `pre` and `post` directories | <ul><li>- [ ] </li></ul> | <ul><li>- [ ] </li></ul> |

## Bugs
- Status check before downloading seems to not be working
- Key validation JS not working
- zipfile doesn't support encryption, needs a new solution
- Unauthorised used can download other files, needs solution (cookie or token)

## Improvements
- Use React instead of controlling views and states just with JQuery
