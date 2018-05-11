# Tricle-Lite - Soft Encryptor

## The Basics
<i>Tricle-Lite</i> is a leaner variation of the <i>Tricle</i> application. <i>Tricle</i> is a python based app for scrambling and unscrambling image files. Scrambling refers to an algorithm that that uses three user given keys to manipulate the pixel positioning in a reversable way, effectively <i>soft-encrypting</i> the image.

This variation of <i>Tricle</i> partly focused on shifting the scrambling algorithm into a more object oriented form. However, the main purpose of this version is to make a more user friendly web interface. The previous web version was bloated, with multiple pages and no clear split between the frontend and the backend.

## The Interface
The app consists of a Django backend which provides a stateful API, and a single page VueJS based web app for interfacing with the API.

## The API - Short and Sweet
To use the application, an account is no longer needed. Which means the API was considerably downsized with some features added to improve user experience.

### The Flow
<ol>
<li><i>post</i> - Post your a set of images, along with the keys, mode, and some additional data</li>
<li><i>load</i> - Run the scrambling process</li>
<li><i>down</i> - Download the scrambled images (up to three times in a 10 minute period, after which they are automatically deleted from the server)</li>
<li><i>done</i> - Manually force the deletion of all images and data from the server, instead of waiting for the daemon<li>
</ol>

## Todo

| Task | Description | In Progress | Done |
| :---: | :--- | :---: | :---: |
| `1` | Add downloads remaining and expiration countdown to download div | <ul><li>- [ ] </li></ul> | <ul><li>- [ ] </li></ul> |
| `2` | Refacture views in tools and add certain methods to the model classes (getStatus, etc) | <ul><li>- [ ] </li></ul> | <ul><li>- [x] </li></ul> |
| `3` | https://www.sitepoint.com/build-javascript-countdown-timer-no-dependencies/ | <ul><li>- [ ] </li></ul> | <ul><li>- [ ] </li></ul> |
| `4` | Password for zipfile if phase isnt local | <ul><li>- [x] </li></ul> | <ul><li>- [ ] </li></ul> |
| `5` | Link to GitHub in dropdown | <ul><li>- [ ] </li></ul> | <ul><li>- [ ] </li></ul> |
| `6` | Delete files once processed | <ul><li>- [ ] </li></ul> | <ul><li>- [x] </li></ul> |
| `7` | Create /iaw (cleanup) view | <ul><li>- [x] </li></ul> | <ul><li>- [ ] </li></ul> |
| `8` | Create /hard (delete and expire everything) view | <ul><li>- [ ] </li></ul> | <ul><li>- [x] </li></ul> |
| `9` | Create `pre` and `post` dirs to store files in | <ul><li>- [ ] </li></ul> | <ul><li>- [ ] </li></ul> |
| `10` | Add v2 seedgen using hashlib and mixed keys | <ul><li>- [ ] </li></ul> | <ul><li>- [ ] </li></ul> |
| `11` | Move form post to separate endpoint | <ul><li>- [ ] </li></ul> | <ul><li>- [x] </li></ul> |
| `12` | Use the zip token to validate the /down request, make it a POST | <ul><li>- [ ] </li></ul> | <ul><li>- [x] </li></ul> |
| `13` | Encrypt the `pre` and `post` directories | <ul><li>- [ ] </li></ul> | <ul><li>- [ ] </li></ul> |
| `14` | Rewrite front end with VueJS | <ul><li>- [x] </li></ul> | <ul><li>- [ ] </li></ul> |
| `15` | Clearly split FE and BE | <ul><li>- [ ] </li></ul> | <ul><li>- [x] </li></ul> |
| `16` | Document API | <ul><li>- [ ] </li></ul> | <ul><li>- [ ] </li></ul> |

Additionally, an endpoint needs to be added which returns the estimated processing time for a url if unprocessed, or the actual processing time if processed. This will require a new model with a one to one look to a url, called a LoadMonitor which will track the time taken and be linked to LoadItem's which contain the file size, and type. 

## Bugs
- Status check before downloading seems to not be working
- Key validation JS not working
- zipfile doesn't support encryption, needs a new solution
- Unauthorised used can download other files, needs solution (cookie or token)

## Improvements
- Use React instead of controlling views and states just with JQuery
