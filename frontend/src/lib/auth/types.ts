export interface AuthUser {
	id: string;
	name: string;
	email: string;
	image: string;
	accessToken: string;
	accessTokenExpires: number;
	refreshToken: string;
}
