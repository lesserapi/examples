from typing import Union
from django.urls.base import reverse
from django.views.generic.base import View
from django.http.request import HttpRequest
from django.shortcuts import render, redirect
from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from .utils import checkUser, checkBranch

# Package Name : lesserapi
# Package Owner :  shervinbdndev
# Package Source : https://github.com/lesserapi/lesserapi/
# Package Owner Github: https://github.com/shervinbdndev/
from lesserapi.github.scraper import GithubScrape
from lesserapi.handlers.user_handler import UserHandler
from lesserapi.handlers.request_handler import RequestHandler







class IndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(
            request=request,
            template_name='index.html',
            context={},
        )
        
    def post(self, request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect]:
        username = request.POST['username']
        if (username is not ''):
            if (checkUser(username=username) == True):
                user_handler: UserHandler =  UserHandler(username=username).serialize()
                request_handler: RequestHandler = RequestHandler(url=user_handler).sendGetRequest(content=True)
                scraper: GithubScrape = GithubScrape(data=request_handler)
                
                scraper.startApi(log=True)
                
                request.session['fullname'] = scraper.fullname
                request.session['followings'] = scraper.followings
                request.session['followers'] = scraper.followers
                request.session['totalRepos'] = scraper.totalRepositories
                request.session['totalSG'] = scraper.totalStarsGiven
                request.session['lyc'] = scraper.lastYearContributions
                request.session['website'] = scraper.website
                request.session['userHasReadme'] = 'Yes' if (scraper.userHasReadMe(username=username)) else 'No'
                request.session['location'] = scraper.location
                request.session['biography'] = scraper.biography
                request.session['ppURL'] = scraper.profilePictureUrl
                request.session['repoNames'] = scraper.repositoriesNames(username=username, ftl=True)
                request.session['userAchvs'] = scraper.userAchievements(username=username)
                request.session['loFollowings'] = scraper.listFollowings(username=username)
                request.session['loFollowers'] = scraper.listFollowers(username=username)
                
                return redirect(to=reverse(viewname='user_results'))
            
            return redirect(to=reverse(viewname='404'))
            
        return render(
            request=request,
            template_name='index.html',
            context={},
        )
        
        

        


class CheckRepoInformationView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(
            request=request,
            template_name='repo_data.html',
            context={},
        )
    
    def post(self, request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect]:
        username, repo_name, branch_name = request.POST['username'], request.POST['reponame'], request.POST['branchname']
        if (username is not '' and repo_name is not '' and branch_name is not ''):
            if (checkUser(username=username) == True and checkBranch(username=username, repo_name=repo_name, branch_name=branch_name)):
                user_handler: UserHandler =  UserHandler(username=username).serialize()
                request_handler: RequestHandler = RequestHandler(url=user_handler).sendGetRequest(content=True)
                scraper: GithubScrape = GithubScrape(data=request_handler)
                
                scraper.startApi(log=True)
                
                request.session['repoName'] = repo_name
                request.session['repoStars'] = scraper.checkRepositoryStars(username=username, repo_name=repo_name)
                request.session['repoPubArch'] = 'Yes' if scraper.isRepositoryPublicArchive(username=username, repo_name=repo_name) else 'No'
                request.session['repoDesc'] = scraper.repositoryDescription(username=username, repo_name=repo_name)
                request.session['repoUsdLangs'] = scraper.repositoryUsedLanguages(username=username, repo_name=repo_name)
                request.session['repoHasLi'] = 'Yes' if scraper.repositoryHasLicense(username=username, repo_name=repo_name) else 'No'
                request.session['repoLiType'] = scraper.repositoryLicenseType(username=username, repo_name=repo_name)
                request.session['lstCmtDate'] = scraper.repositoryLastCommitDateOnBranch(username=username, repo_name=repo_name, branch_name=branch_name)
                request.session['repoBranchesCount'] = scraper.repositoryBranchesCount(username=username, repo_name=repo_name)
                request.session['repoBranches'] = scraper.listRepositoryBranches(username=username, repo_name=repo_name)
                request.session['loRepoWathcers'] = scraper.listRepositoryWatchers(username=username, repo_name=repo_name)
                
                return redirect(to=reverse(viewname='repo_results'))
            
            return redirect(to=reverse(viewname='404'))
        
        return render(
            request=request,
            template_name='repo_data.html',
            context={},
        )





class UserResultsView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(
            request=request,
            template_name='user_results.html',
            context={},
        )
        



class RepoResultsView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(
            request=request,
            template_name='repo_results.html',
            context={},
        )
        



class E404View(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(
            request=request,
            template_name='404.html',
            context={},
        )