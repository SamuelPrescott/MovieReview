import { Component } from '@angular/core';
import { WebService } from './web.service';
import { ActivatedRoute } from '@angular/router';
import { FormBuilder, Validators } from '@angular/forms';
import { AuthService } from '@auth0/auth0-angular';
import { analyzeAndValidateNgModules } from '@angular/compiler';
import { delay } from 'rxjs';

@Component({
    selector: 'show',
    templateUrl: './show.component.html',
    styleUrls: ['./show.component.css']
})
export class showComponent {

    reviewsForm: any;
    updateForm: any;
    showMe: boolean = false

    constructor(private webService: WebService,
        private route: ActivatedRoute,
        private formBuilder: FormBuilder,
        public authService: AuthService) { }

    ngOnInit() {




        this.reviewsForm = this.formBuilder.group({
            username: ['', Validators.required],
            reviews: ['', Validators.required],
            stars: 5
        });

        this.show_list = this.webService.getShow(this.route.snapshot.params['id']);
        this.reviews = this.webService.getReviews(this.route.snapshot.params['id']);

        this.updateForm = this.formBuilder.group({
            title: ['',Validators.required],
            listed_in: ['',Validators.required],
            director: ['',Validators.required],
            cast: ['',Validators.required],
            duration: [''],
            release_year: [''],
            description: ['',Validators.required],
            url: [''],
          });

        this.webService.getShow(this.route.snapshot.params['id']);

        

    }

    onSubmit() {
        this.webService.postReview(this.reviewsForm.value)
            .subscribe((Response: any) => {
                this.reviewsForm.reset();
                this.reviews = this.webService.getReviews(this.route.snapshot.params['id']);
            })

    }

    toggleEdit() {
        this.showMe = !this.showMe
    }

    onUpdate(){
        console.log(this.updateForm.value)
        this.webService.updateShow(this.updateForm.value).subscribe((Response: any)=>{
        this.updateForm.reset();
        this.show_list = this.webService.getShows(this.route.snapshot.params['id']);
            })
        

        }

    onDelete(showID: any){
        console.log(showID)
        this.webService.deleteShow(showID)
    }

    onDeleteReview(showID: any, review:any){
        console.log(showID)
        this.webService.deleteReview(showID, review)
        
    }

    isInvalid(control: any) {
        return this.reviewsForm.controls[control].invalid &&
            this.reviewsForm.controls[control].touched;
    }

    isUntouched() {
        return this.reviewsForm.controls.username.pristine ||
            this.reviewsForm.controls.reviews.pristine;
    }

    isIncomplete() {
        return this.isInvalid('username') ||
            this.isInvalid('reviews') ||
            this.isUntouched();
    }
    isInvalidShow(control: any) {
        return this.updateForm.controls[control].invalid && this.updateForm.controls[control].touched;
      }
    
      isUntouchedShow() {
        
         return this.updateForm.controls.title.pristine ||
         this.updateForm.controls.listed_in.pristine ||
         this.updateForm.controls.director.pristine ||
         this.updateForm.controls.cast.pristine ||
         this.updateForm.controls.description.pristine ||
         this.updateForm.controls.year_released.pristine ||
         this.updateForm.controls.duration.pristine ||
         this.updateForm.controls.url.pristine;

      }
    
      IncompleteShow() {
          this.isInvalidShow('title') ||
          this.isInvalidShow('release_year') ||
          this.isInvalidShow('duration') ||
          this.isInvalidShow('director') ||
          this.isInvalidShow('cast') ||
          this.isInvalidShow('description') ||
          this.isInvalidShow('url') ||
          this.isUntouchedShow();
      }

    
    show_list: any = [];
    reviews: any = [];

}
