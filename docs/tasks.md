## Auth
- [x] Routes
  - [x] Token
  - [x] Refresh
- [x] Session
  - [x] Access_token
  - [x] Refresh_token
- [x] Token JWT
  - [x] Expire
  - [x] Body
  - [x] Encode
  - [x] Decode
- [x] Models
  - [x] Token
  - [x] TokenData
  - [x] TokenRefresh

## Users
- [x] Routes 
  - [x] Create
  - [x] Delete
  - [x] Get all profiles
  - [x] Get profile by username
  - [x] Get account data
  - [x] Update account
  - [x] Update profile
  - [x] Update birthday
- [x] Models
  - [x] UserModel
  - [x] ProfileModel
  - [x] BirthdayModel
  - [x] AccessModel
  - [x] Request
    - [x] RequestCreateAccount
    - [x] RequestProfile
    - [x] RequestBirthday
    - [x] RequestAccess
    - [x] Update Account
    - [x] UpdateAvatar
    - [x] UpdateAccess
  - [x] Response
    - [x] ProfileResponse
    - [x] AccountDataResponse

## Password
- [x] Routes
  - [x] Update
  - [x] Recover
  - [x] Reset
- [x] Models
  - [x] RecoverPassword
  - [x] UpdatePassword

## Posts
- [x] Routes
  - [x] Create
  - [x] Delete
  - [x] Update
  - [x] Get all
  - [x] Get by id
  - [x] Get all by username
  - [x] Add like
- [x] Models
  - [x] PostModel
  - [x] PostResponse
  - [x] PostRequest
  - [x] LikeModel

## Replies
- [x] Routes
  - [x] Create
  - [x] Delete
  - [x] Update
  - [x] Get by id
  - [x] Get all by post_id
  - [x] Add like
- [x] Models
  - [x] ReplyModel
