import { Component, OnInit } from '@angular/core';
import { Router , ActivatedRoute } from "@angular/router";
import { AppService } from "../../app.service";
import {Location} from '@angular/common';
// import * as test from "../../../scripts";
import * as $ from 'jquery' 
export class NewImg {
  public image: any;
  public medicinename: any;
}
@Component({
  selector: 'app-admindash',
  templateUrl: './admindash.component.html',
  styleUrls: ['./admindash.component.css']
})
export class AdmindashComponent implements OnInit {
  parseusername : any;
  data:any;
  sublinks:any;
  newimg = new NewImg();
  userid:any;
  linkid:any;
  linkname:any;
  linkurl:any;
  no_of_links:number;
  img:any;
  image:any;
  imageUrl:any;
  ImageBaseData:any;
  sscore:any;
  
  loader = true;
  constructor(private rt:Router , private router : ActivatedRoute, private service : AppService,private _location: Location) { 
    this.router.params.subscribe(params=>{
      this.parseusername = params.username;
      if(JSON.parse(window.localStorage.getItem('un'))== this.parseusername){
        this.userid=JSON.parse(window.localStorage.getItem('id'));
      }
    })
  }
  
  ngOnInit() {
    this.service.mainlink(this.parseusername).subscribe(res=>{
      this.sscore = res[0].creditScore;
    })
    this.ImageBaseData = 'https://i.ibb.co/34XWSYz/ii.jpg';
  }
  handleFileInput(files: FileList) {
    var me = this;
    let file = files[0];
    let reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = function () {
      // console.log(reader.result);
      me.ImageBaseData=reader.result;
    };
    reader.onerror = function (error) {
      console.log('Error: ', error);
    };
 }
  editProficPic(){
    this.newimg.image = this.ImageBaseData;
    this.service.updatePic(this.parseusername, this.newimg).subscribe(res=>{
      window.location.reload();
    })
  }
  getLinkInfo(link,name,url){
    this.linkid = link;
    this.linkname=name;
    this.linkurl = url;
    console.log(name,url);
  }
  deleteLink(){
    this.service.delLink(this.linkid).subscribe(result=>{
      window.location.reload();
    })
  }
  gotolink(link)
  {
    window.open(link);
  }
  gotomainlink()
  {
    window.open('https://weblink-analysis.vercel.app/'+this.parseusername);
  }
}