export default {
  name: "StartButton",
  template:`<div class="flex-container-row">
            <div @click="$emit('starting')">
              <svg version="1.1"
                   baseProfile="full"
                   width="300" height="500"
                   xmlns="http://www.w3.org/2000/svg">

                <rect rx="15" ry="15" width="100%" height="100%" fill="red" />
                <circle cx="150" cy="100" r="80" fill="green" />
                <text x="150" y="125" font-size="60" text-anchor="middle" fill="white">Start</text>

              </svg>
              </div>
            </div>`
};
