import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';

@Injectable()
export class WebService {

    private showID: any;

    constructor(private http: HttpClient){

    }

    show_list: any;

    getShows(page: number){
        return this.http.get('http://localhost:5000/api/v1.0/shows?pn=' + page);  
    }

    getShow(id: any){
        this.showID = id;
        return this.http.get('http://localhost:5000/api/v1.0/shows/' + id );
    }

    getReviews(id: any){
        return this.http.get('http://localhost:5000/api/v1.0/shows/' + id + "/reviews");
    }

    getTvShows(page: number){
        return this.http.get('http://localhost:5000/api/v1.0/TvShows?pn=' + page);
    }

    getMovies(page: number){
        return this.http.get('http://localhost:5000/api/v1.0/movies?pn=' + page);
    }

    postReview(review: any){
        let postData = new FormData();
        postData.append("username", review.username);
        postData.append("text", review.reviews);
        postData.append("stars", review.stars);

        let today = new Date();
        let todayDate = today.getDate() + "/" + 
                        today.getMonth() + "/" +
                        today.getFullYear();
        postData.append("date", todayDate);

        return this.http.post('http://localhost:5000/api/v1.0/shows/' +
                                this.showID + '/reviews', postData);
    }

    postShow(add:any){
        let postData = new FormData();
        postData.append("type", add.type);
        postData.append("title", add.title);
        postData.append("director", add.director);
        postData.append("cast", add.cast);
        postData.append("release_year", add.release_year);
        postData.append("listed_in", add.listed_in);
        postData.append("description", add.description);
        postData.append("duration", add.duration);
        postData.append("url", add.url);
     
        return this.http.post('http://localhost:5000/api/v1.0/shows', postData);
       }

    deleteReview(id:any, review:any){
         this.http.delete('http://localhost:5000/api/v1.0/shows/' + id + '/reviews/' + review).subscribe((Response: any) =>{
            window.location.reload()
        })
           
        
    }

    deleteShow(showID:any){
        
        this.http.delete('http://localhost:5000/api/v1.0/shows/' + showID).subscribe((Response: any)=>{
        })
    
    }

    updateShow(update: any){
        let putData = new FormData();
        putData.append("title", update.title);
        putData.append("director", update.director);
        putData.append("cast", update.cast);
        putData.append("release_year", update.release_year);
        putData.append("listed_in", update.listed_in);
        putData.append("description", update.description);
        putData.append("duration", update.duration);
        putData.append("url", update.url);
        
        return this.http.put('http://localhost:5000/api/v1.0/shows/' + this.showID, putData,);{
        
    }
    }
    
}
