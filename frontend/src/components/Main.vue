<script>
import axios from 'axios';
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
export default {
  components: { VueDatePicker },
  data() {
    return {
      activeItemModal: false,
      editItemModal: false,
      addItemform: {
        title: '',
        body: '',
        period: '',
        start: Date(),
        end: Date(),
      },
      editItemform: {
        id: '',
        title: '',
        body: '',
        period: '',
        start: Date(),
        end: Date(),
      },
      items: [],
    }
  },
  methods: {
    addItem(payload) {
      const path = 'http://127.0.0.1:5000/items';
      axios.post(path, payload)
          .then(() => {
            this.getItems();
          })
          .catch((error) => {
            console.log(error);
            this.getItems();
          });
    },
    getItems() {
      const path = 'http://127.0.0.1:5000/items';
      axios.get(path)
          .then((res) => {
            this.items = res.data.items;
          })
             .catch((error) => {
          console.error(error);
        });
    },
    addSumbit() {
      this.switchAddItemModal();
      const payload = {
        title: this.addItemform.title,
        body: this.addItemform.body,
        period: this.addItemform.period,
        start: this.addItemform.start,
        end: this.addItemform.end
      };
      this.addItem(payload);
      this.initForm();
    },
    editSubmit () {
      this.switchEditItemModal(null);
      const payload = {
        title: this.editItemform.title,
        body: this.editItemform.body,
        period: this.editItemform.period,
        start: this.editItemform.start,
        end: this.editItemform.end
      };
      this.updateItem(payload, this.editItemform.id)
    },
    initForm() {
      this.addItemform.title = '';
      this.addItemform.body = '';
      this.addItemform.period = '';
      this.addItemform.start = Date()
      this.addItemform.end = Date()
      this.editItemform.id = '';
      this.editItemform.title = '';
      this.editItemform.body = '';
      this.editItemform.period = '';
      this.editItemform.start = Date()
      this.editItemform.end = Date()
    },
    updateItem(payload, itemID) {
      const path = `http://127.0.0.1:5000/items/${itemID}`;
      axios.put(path, payload)
          .then(() => {
            this.getItems();
              })
      .catch((error) => {
        console.error(error);
        this.getItems();
      })
    },
    switchAddItemModal() {
      const body = document.querySelector('body');
      this.activeItemModal = !this.activeItemModal;
      if (this.activeItemModal) {
        body.classList.add('modal-open');
      } else {
        body.classList.remove('modal-open');
      }
    },
    switchEditItemModal(item) {
      if (item) {
        this.editItemform = item;
      }
      const body = document.querySelector('body');
      this.editItemModal = !this.editItemModal;
      if (this.editItemModal) {
        body.classList.add('modal-open')
      } else {
        body.classList.remove('modal-open')
      }
    }
  },
  created() {
    this.getItems()
    }
}
</script>

<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-15">
        <div class="text-center">
        <h1>Гарантийник</h1>
        <p class="lead">Сервис для хранения гарантий</p>
        </div>
        <hr>
        <!-- Кнопка-триггер модального окна -->
        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#staticBackdrop" @click="switchAddItemModal">
          Создать гарантию
        </button>
        <br><br>
  </div>
      <!-- Форма отображения данных -->
        <div class="row" v-for="i in Math.ceil(items.length / 4)" >
          <div class="col-3" v-for="item in items.slice((i - 1) * 4, i * 4)">
            <div class="card">
              <div class="card-body">
                    <h5 class="card-title"> {{ item.title }}</h5>
                    <p class="card-text"> {{ item.body }}</p>
                    <p class="card-text"> {{ item.period }}</p>
                    <p class="card-calendar-start"> {{ item.start }}</p>
                    <p class="card-calendar-finish"> {{ item.end }}</p>
                    <button type="button" class="btn btn-primary" data-bs-toggle="modal" @click="switchEditItemModal(item)" data-bs-target="#exampleModal" >
                      Обновить
                    </button>
                    <button type="button" class="btn btn-danger">Удалить</button>
              </div>
            </div>
            </div>
        </div>
      </div>
    </div>

  <!-- Модальное окно 'Добавление'-->
  <div class="modal fade"
     ref="addItemModal"
     :class="{show: activeItemModal, 'd-block': activeItemModal}"
     id="staticBackdrop" data-bs-backdrop="static"
     data-bs-keyboard="false"
     tabindex="-1"
     aria-labelledby="staticBackdropLabel"
     aria-hidden="false">
  <div class="modal-dialog"
       role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h1 class="modal-title fs-5" id="exampleModalLabel">Создание гарантии:</h1>
        <button type="button" class="btn-close" data-bs-dismiss="modal" @click="switchAddItemModal" aria-label="Закрыть"></button>
      </div>
      <div class="modal-body">
          <div class="mb-3">
            <label for="recipient-name" class="col-form-label">Название: </label>
            <input type="text" v-model="addItemform.title" class="form-control" placeholder="Введите название гарантии" id="recipient-name">
          </div>
          <div class="mb-3">
            <label for="exampleFormControlTextarea1" class="form-label">Описание: </label>
            <textarea class="form-control" v-model="addItemform.body" id="exampleFormControlTextarea1" placeholder="Введите описание гарантии" rows="3"></textarea>
          </div>
          <div class="mb-3">
            <label for="period" class="form-label">Период гарантии: </label>
            <input type="text"  class="form-control" v-model="addItemform.period" id="period" placeholder="Введите период гарантии">
          </div>
            <div class="mb-3">
            <label for="addStart" class="form-label" >Начало гарантии: </label>
            <VueDatePicker v-model="addItemform.start" id="addStart" locale="rus" model-type="yyyy/MM/dd" :enable-time-picker="false" placeholder="Дата начала гарантии"></VueDatePicker>
            </div>
          <div class="mb-3" >
            <label for="endStart" class="form-label" >Окончание гарантии: </label>
            <VueDatePicker v-model="addItemform.end" id="endStart" locale="rus" model-type="yyyy/MM/dd" :enable-time-picker="false" placeholder="Дата окончания гарантии"></VueDatePicker>
          </div>
        </div>
          <div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="switchAddItemModal">Закрыть</button>
        <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="addSumbit">Сохранить</button>
      </div>
    </div>
  </div>
</div>

    <!-- Модальное окно 'Редактура'-->
<div class="modal fade" id="exampleModal" :class="{show: editItemModal,
     'd-block': editItemModal}" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h1 class="modal-title fs-5" id="exampleModalLabel">Изменение гарантии: </h1>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <div class="mb-3">
          <label for="editTitle" class="form-label">Изменить заголовок: </label>
          <input
            type="text"
            class="form-control"
            id="editTitle"
            v-model="editItemform.title"
            placeholder="Введите заголовок">
        </div>
        <div class="mb-3">
          <label for="editBody" class="form-label">Изменить описание: </label>
          <textarea
            type="text"
            class="form-control"
            id="editBody"
            v-model="editItemform.body"
            rows="3">
          </textarea>
        </div>
        <div class="mb-3">
          <label for="period" class="form-label">Изменить период: </label>
          <input
            type="text"
            class="form-control"
            id="period"
            v-model="editItemform.period">
        </div>
        <div class="mb-3">
          <label for="start" class="form-label"  >Изменить начало гарантии: </label>
          <VueDatePicker id="start" v-model="editItemform.start" locale="rus" model-type="yyyy/MM/dd" :enable-time-picker="false" ></VueDatePicker>
        </div>
        <div class="mb-3">
          <label for="end" class="form-label">Изменить конец гарантии: </label>
          <VueDatePicker id="end" v-model="editItemform.end" locale="rus" model-type="yyyy/MM/dd" :enable-time-picker="false" ></VueDatePicker>
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="switchEditItemModal" >Закрыть</button>
        <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="editSubmit">Подтвердить</button>
      </div>
    </div>
  </div>
</div>
</template>
<style scoped>

</style>