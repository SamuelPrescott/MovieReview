import { Component } from '@angular/core';
import { WebService } from './web.service';
import { FormsModule } from '@angular/forms';
import { filter } from 'rxjs';
import { AuthService } from '@auth0/auth0-angular';
import { FormBuilder, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';


@Component({
  selector: 'shows',
  templateUrl: './shows.component.html',

  styleUrls: ['./shows.component.css'],
  template: `
  <ul>
    <li *ngFor="let item of collection | paginate: { itemsPerPage: 6, currentPage: page }"> ... </li>
  </ul>
             
  <pagination-controls (pageChange)="p = $event"></pagination-controls>
  `
})
export class showsComponent {

  
  addForm: any;

  constructor(public webService: WebService,
    public authService: AuthService,
    private route: ActivatedRoute,
    private formBuilder: FormBuilder) {}



    
  

   ngOnInit() {


    this.addForm = this.formBuilder.group({
      type: ['',Validators.required],
      title: ['',Validators.required],
      listed_in: ['',Validators.required],
      director: ['',Validators.required],
      cast: ['',Validators.required],
      description: ['',Validators.required],
      url: [''],
    });




    if (sessionStorage['page']) {
      this.page = sessionStorage['page'];
    }
    this.webService.getShows(this.page);
  


    

    this.show_list = this.webService.getShows(this.page);
  }

  onSubmit() {
    console.log(this.addForm.value)
    this.webService.postShow(this.addForm.value).subscribe(( Response: any)=> {
    this.addForm.reset();
    this.show_list = this.webService.getShow(this.route.snapshot.params['id'])
    
    })
  }

  isInvalid(control: any,) {
    return this.addForm.controls[control].invalid && this.addForm.controls[control].touched;
  }

  isUntouched() {
    return this.addForm.controls.username.pristine || this.addForm.controls.text.pristine;
  }

  isIncompleteShow() {
    return this.isInvalid('type') ||
      this.isInvalid('title') ||
      this.isInvalid('director') ||
      this.isInvalid('cast') ||
      this.isInvalid('description') ||
      this.isInvalid('url') ||
      this.isUntouched();
  }

  previousPage() {
    if (this.page > 1) {
      this.page = this.page - 1;
      this.show_list = this.webService.getShows(this.page);
    }
  }
  nextPage() {
    this.page = this.page + 1;
    this.show_list = this.webService.getShows(this.page);
  }

  




  show_list: any = [];
  page: number = 1;

}
