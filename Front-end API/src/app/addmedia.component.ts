import { Component } from '@angular/core';
import { WebService } from './web.service';
import { ActivatedRoute } from '@angular/router';
import { FormBuilder, Validators } from '@angular/forms';
import { AuthService } from '@auth0/auth0-angular';

@Component({
  selector: 'addmedia',
  templateUrl: './addmedia.component.html',
  styleUrls: ['./addmedia.component.css']
})
export class addmediaComponent {

    addForm: any;

    constructor(public webService: WebService,
        public authService : AuthService,
        private route: ActivatedRoute,
        private formBuilder: FormBuilder){}

    async ngOnInit() {


        this.addForm = this.formBuilder.group({
          type: ['',Validators.required],
          title: ['',Validators.required],
          listed_in: ['',Validators.required],
          director: ['',Validators.required],
          cast: ['',Validators.required],
          duration:['',Validators.required],
          release_year:['',Validators.required],
          description: ['',Validators.required],
          url: ['',Validators.required],
        });


    }
    onSubmit() {
        console.log(this.addForm.value)
        this.webService.postShow(this.addForm.value).subscribe(( Response: any)=> {
        this.addForm.reset();
        // this.show_list = this.webService.getShow(this.route.snapshot.params['id'])
        
        })
      }

      isInvalid(control: any) {
        return this.addForm.controls[control].invalid && this.addForm.controls[control].touched;
      }
    
      isUntouched() {
         this.addForm.controls.title.pristine ||
         this.addForm.controls.director.pristine ||
         this.addForm.controls.cast.pristine ||
         this.addForm.controls.description.pristine ||
         this.addForm.controls.release_year.pristine ||
         this.addForm.controls.duration.pristine ||
         this.addForm.controls.url.pristine;

      }
    
      isIncompleteShow() {
          return this.isInvalid('title') ||
          this.isInvalid('release_year') ||
          this.isInvalid('duration') ||
          this.isInvalid('director') ||
          this.isInvalid('cast') ||
          this.isInvalid('url') ||
          this.isInvalid('description') ||
          this.isUntouched();
      }
    //   show_list: any = [];
      
}