<template>
  <div class="pricing-wrapper">
    <div class="header-container">
      <h1>BTC_USD price Lists</h1>
    </div>

    <div class="search-container">
      <input :value="searchValue" placeholder="please enter search value" @input="searchChange" />
    </div>

    <table class="table-container">
      <tr>
        <th>Date</th>
        <th>Open</th>
        <th>Close</th>
        <th>High</th>
        <th>Low</th>
        <th>Volume</th>
        <th>delete</th>
      </tr>

      <tr v-for="itemData in showData" v-bind:key="itemData.id">
        <td> {{ itemData.Date }} </td>
        <td> <input :value="itemData.Open" type="number" v-on:blur="itemUpdate(itemData.id, 'Open')" /> </td>
        <td> <input :value="itemData.Close" type="number" v-on:blur="itemUpdate(itemData.id, 'Close')" /> </td>
        <td> <input :value="itemData.High" type="number" v-on:blur="itemUpdate(itemData.id, 'High')" /> </td>
        <td> <input :value="itemData.Low" type="number" v-on:blur="itemUpdate(itemData.id, 'Low')" /> </td>
        <td> <input :value="itemData.Volume" type="number" v-on:blur="itemUpdate(itemData.id, 'Volume')" /> </td>

        <td>
          <svg fill="#000000" version="1.1" v-on:click="itemDelete(itemData.id)"
            xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 482.428 482.429" xml:space="preserve">
            <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
            <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
            <g id="SVGRepo_iconCarrier">
              <g>
                <g>
                  <path
                    d="M381.163,57.799h-75.094C302.323,25.316,274.686,0,241.214,0c-33.471,0-61.104,25.315-64.85,57.799h-75.098 c-30.39,0-55.111,24.728-55.111,55.117v2.828c0,23.223,14.46,43.1,34.83,51.199v260.369c0,30.39,24.724,55.117,55.112,55.117 h210.236c30.389,0,55.111-24.729,55.111-55.117V166.944c20.369-8.1,34.83-27.977,34.83-51.199v-2.828 C436.274,82.527,411.551,57.799,381.163,57.799z M241.214,26.139c19.037,0,34.927,13.645,38.443,31.66h-76.879 C206.293,39.783,222.184,26.139,241.214,26.139z M375.305,427.312c0,15.978-13,28.979-28.973,28.979H136.096 c-15.973,0-28.973-13.002-28.973-28.979V170.861h268.182V427.312z M410.135,115.744c0,15.978-13,28.979-28.973,28.979H101.266 c-15.973,0-28.973-13.001-28.973-28.979v-2.828c0-15.978,13-28.979,28.973-28.979h279.897c15.973,0,28.973,13.001,28.973,28.979 V115.744z">
                  </path>
                  <path
                    d="M171.144,422.863c7.218,0,13.069-5.853,13.069-13.068V262.641c0-7.216-5.852-13.07-13.069-13.07 c-7.217,0-13.069,5.854-13.069,13.07v147.154C158.074,417.012,163.926,422.863,171.144,422.863z">
                  </path>
                  <path
                    d="M241.214,422.863c7.218,0,13.07-5.853,13.07-13.068V262.641c0-7.216-5.854-13.07-13.07-13.07 c-7.217,0-13.069,5.854-13.069,13.07v147.154C228.145,417.012,233.996,422.863,241.214,422.863z">
                  </path>
                  <path
                    d="M311.284,422.863c7.217,0,13.068-5.853,13.068-13.068V262.641c0-7.216-5.852-13.07-13.068-13.07 c-7.219,0-13.07,5.854-13.07,13.07v147.154C298.213,417.012,304.067,422.863,311.284,422.863z">
                  </path>
                </g>
              </g>
            </g>
          </svg>
        </td>
      </tr>
    </table>

    <div class="footer-container">
      <div class="buttons-container">
        <button class="back-btn" v-on:click="nextOnClick(-1)">Back</button>
        <button class="next-btn" v-on:click="nextOnClick(1)">Next</button>
      </div>

      <div class="page-counter">
        <span>page {{ pageNumber }}</span>
        <span>total page {{ getTotalPage() }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'PriceListComponent',
  data () {
    return {
      data: [],
      showData: [],
      pageNumber: 1,
      pageCount: 10,
      searchValue: ''
    }
  },
  methods: {
    // api function
    getPriceList: function () {
      axios.get('http://127.0.0.1:8000/getPrice')
        .then((response) => {
          this.pageNumber = 1
          this.searchValue = ''
          this.data = response.data
          this.showData = response.data.slice(0, this.pageCount)
        })
    },
    itemDelete: function (id) {
      axios.post('http://127.0.0.1:8000/delete/', { key: id })
        .then((response) => {
          this.data = response.data
          let tempData = this.getSearchValue()
          var totalPage = Math.ceil(tempData.length / this.pageCount)
          if (totalPage <= this.pageNumber) {
            this.pageNumber = totalPage
          }

          let start = (this.pageNumber - 1) * this.pageCount
          let endCount = this.pageNumber * this.pageCount
          this.showData = tempData.slice(start, endCount)
        })
    },
    itemUpdate: function (id, key) {
      let value = parseFloat(event.target.value)
      axios.post('http://127.0.0.1:8000/update/', { id: id, key: key, value: value })
        .then((response) => {
          this.data = response.data
          let tempData = this.getSearchValue()
          var totalPage = Math.ceil(tempData.length / this.pageCount)
          if (totalPage <= this.pageNumber) {
            this.pageNumber = totalPage
          }

          let start = (this.pageNumber - 1) * this.pageCount
          let endCount = this.pageNumber * this.pageCount
          this.showData = tempData.slice(start, endCount)
          console.log(response)
        })
    },
    // front-end function
    nextOnClick: function (flag) {
      let tempData = this.getSearchValue()
      let totalPage = Math.ceil(tempData.length / this.pageCount)
      if (totalPage < (this.pageNumber + flag)) return
      if (!(this.pageNumber + flag)) return

      this.pageNumber += flag
      if (totalPage <= this.pageNumber) this.pageNumber = totalPage
      let start = (this.pageNumber - 1) * this.pageCount
      let endCount = this.pageNumber * this.pageCount
      this.showData = tempData.slice(start, endCount)
    },
    searchChange: function (e) {
      this.searchValue = e.target.value
      let tempData = this.getSearchValue()
      var totalPage = Math.ceil(tempData.length / this.pageCount)
      if (totalPage <= this.pageNumber) this.pageNumber = totalPage
      if (!!totalPage && !this.pageNumber) this.pageNumber = 1

      let start = (this.pageNumber - 1) * this.pageCount
      let endCount = this.pageNumber * this.pageCount
      this.showData = tempData.slice(start, endCount)
    },
    getSearchValue: function () {
      let totalData = []
      this.data.forEach((item) => {
        let check = Object.values(item).join('').indexOf(this.searchValue)
        if (check !== -1) totalData.push(item)
      })

      return totalData
    },
    getTotalPage: function () {
      let tempData = this.getSearchValue()
      var totalPage = Math.ceil(tempData.length / this.pageCount)
      return totalPage
    }
  },
  beforeMount () {
    this.getPriceList()
  }
}
</script>

<style>
.header-container h1 {
  font-size: 40px;
  font-weight: 900;
  color: #080a2f;
  text-shadow: 3px 4px 5px rgba(117, 129, 60, 0.849);
}

.pricing-wrapper {
  gap: 10px;
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  padding: 0px 200px;
}

.search-container {
  width: 100%;
  height: 50px;
  display: flex;
  flex-direction: column;

  border: 1px solid #04AA6D;
}

input {
  width: 100%;
  height: 100%;
  border: unset;
  outline: unset;
  padding: 0px 10px;
  background-color: unset;
}

.table-container {
  width: 100%;
}

.table-container th {
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: left;
  background-color: #04AA6D;
  color: white;
}

.table-container tr:hover {
  background-color: #ddd;
}

.table-container tr:nth-child(even) {
  background-color: #f2f2f2;
}

.table-container td,
.table-container th {
  border: 1px solid #ddd;
  padding: 8px;
}

tr td:first-child {
  width: 200px;
}

.footer-container {
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.buttons-container {
  flex: 1;
  gap: 10px;
  display: flex;
  flex-direction: row;
}

.back-btn,
.next-btn {
  width: 100%;
  max-width: 200px;
  padding: 20px 20px;
  color: white;
  border: unset;
  cursor: pointer;
}

.back-btn:hover,
.next-btn:hover {
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
}

.back-btn {
  background-color: rgb(192, 57, 52);
}

.next-btn {
  background-color: #04AA6D;
}

.page-counter {
  display: flex;
  flex-direction: row;
  gap: 10px;
}

td svg {
  width: 15px;
  cursor: pointer;
}

td svg:hover {
  fill: red;
}

td:last-child {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>
