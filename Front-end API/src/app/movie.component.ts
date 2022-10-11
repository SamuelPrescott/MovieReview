import { Component } from '@angular/core';
import { WebService } from './web.service';
import { ActivatedRoute } from '@angular/router';
import { FormBuilder, Validators } from '@angular/forms';
import { AuthService } from '@auth0/auth0-angular';

@Component({
  selector: 'movie',
  templateUrl: './movie.component.html',
  styleUrls: ['./movie.component.css']
})
export class movieComponent {

    constructor(public webService: WebService,
        public authService: AuthService,
        private route: ActivatedRoute){}


    
        ngOnInit(){
            if (sessionStorage['page']) {
                this.page = sessionStorage['page'];
              }
              this.webService.getMovies(this.page);
            
          
          
              
          
              this.show_list = this.webService.getMovies(this.page);
        }

        

    previousPage() {
        if (this.page > 1) {
          this.page = this.page - 1;
          this.show_list = this.webService.getMovies(this.page);
        }
      }
      nextPage() {
        this.page = this.page + 1;
        this.show_list = this.webService.getMovies(this.page);
      }
    
      
    
    
    
    
      show_list: any = [];
      page: number = 1;
    
}
